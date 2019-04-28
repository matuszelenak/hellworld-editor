from functools import wraps

from django.contrib import admin, messages

# Register your models here.
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse

from submit.models import Task, Submit, SubmitScore
from submit.tasks import UpdateTaskInputs


def single_item_action(method_or_name=None, select_for_update=False):
    """
    Decorator for admin actions that forces only one selected item

    Usage:

    @single_item_action
    def admin_action(self, request, item):
        ...

    @single_item_action(select_for_update=True)
    def admin_action(self, request, item):
        ...
        (update item here)
        ...

    If wrapped function returns None, redirect to admin detail is used
    """
    def decorator(method):
        @wraps(method)
        def wrapper(admin_obj, request, queryset, *args, **kwargs):
            if len(queryset) != 1:
                admin_obj.message_user(request, 'Feature is available only for one item at a time', level=messages.ERROR)
            else:
                if select_for_update:
                    obj = queryset.model.objects.select_for_update().get(pk=queryset)
                else:
                    obj = queryset.get(pk=queryset)

                response = method(admin_obj, request, obj)
                if response:
                    return response
                else:
                    return HttpResponseRedirect(reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name), args=[obj.pk]))

        return wrapper

    if callable(method_or_name):
        return decorator(method_or_name)
    else:
        return decorator


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    actions = ('fetch_inputs',)

    @transaction.atomic
    def fetch_inputs(self, request, queryset):
        transaction.on_commit(lambda: UpdateTaskInputs().delay(task_pks=list(queryset.values_list('pk', flat=True))))


@admin.register(Submit)
class SubmitAdmin(admin.ModelAdmin):
    actions = ('score', )

    def score(self, request, queryset):
        for s in queryset:
            s.run_scoring()


@admin.register(SubmitScore)
class SubmitScoreAdmin(admin.ModelAdmin):
    pass
