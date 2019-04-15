from django.contrib import admin

# Register your models here.
from django.db import transaction

from submit.models import Task, Submit, SubmitScore


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Submit)
class SubmitAdmin(admin.ModelAdmin):
    actions = ('score', )

    def score(self, request, queryset):
        for s in queryset:
            s.run_scoring()


@admin.register(SubmitScore)
class SubmitScoreAdmin(admin.ModelAdmin):
    pass
