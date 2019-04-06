from django.contrib import admin
from .models import DiseaseInstance, DiseaseClass, DiseaseTransmit, MedicineClass, MedicineEffect


@admin.register(DiseaseTransmit)
class DiseaseTransmitAdmin(admin.ModelAdmin):
    pass


@admin.register(DiseaseInstance)
class DiseaseInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(DiseaseClass)
class DiseaseClassAdmin(admin.ModelAdmin):
    pass


@admin.register(MedicineClass)
class MedicineClassAdmin(admin.ModelAdmin):
    pass


@admin.register(MedicineEffect)
class MedicineEffectAdmin(admin.ModelAdmin):
    pass

