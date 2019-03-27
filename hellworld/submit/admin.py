from django.contrib import admin

# Register your models here.
from submit.models import Task, Submit, SubmitScore


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Submit)
class SubmitAdmin(admin.ModelAdmin):
    pass


@admin.register(SubmitScore)
class SubmitScoreAdmin(admin.ModelAdmin):
    pass
