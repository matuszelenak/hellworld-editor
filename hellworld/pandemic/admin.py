from django.contrib import admin
from .models import DiseaseInstance, DiseaseClass, DiseaseTransmit


@admin.register(DiseaseTransmit)
class DiseaseTransmitAdmin(admin.ModelAdmin):
    pass


@admin.register(DiseaseInstance)
class DiseaseInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(DiseaseClass)
class DiseaseClassAdmin(admin.ModelAdmin):
    pass
