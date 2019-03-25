from django.contrib import admin

# Register your models here.
from submit.models import Task, Submit


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Submit)
class SubmitAdmin(admin.ModelAdmin):
    pass
