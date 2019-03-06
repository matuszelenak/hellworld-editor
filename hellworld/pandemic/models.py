from django.db import models

# Create your models here.


class DiseaseClass(models.Model):
    TYPE_INFECTIOUS = 0
    TYPE_DEGENERATIVE = 1

    TYPES = (
        ('Infectious', TYPE_INFECTIOUS),
        ('Degenerative', TYPE_DEGENERATIVE)
    )

    name = models.TextField(null=False)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES)


class DiseaseTransmit(models.Model):
    disease_id = models.ForeignKey('pandemic.DiseaseClass', related_name='transmissions', on_delete=models.CASCADE)
    tag_id = models.ForeignKey('people.BluetoothTag', related_name='transmissions', on_delete=models.CASCADE)
    severity = models.IntegerField(null=False)


class MedicineClass(models.Model):
    name = models.TextField(null=False)
    description = models.TextField()


class MedicineEffect(models.Model):
    medicine_id = models.ForeignKey('pandemic.MedicineClass', related_name='applications', on_delete=models.CASCADE)
    disease_id = models.ForeignKey('pandemic.DiseaseClass', related_name='applied_medicines', on_delete=models.CASCADE)
    strength = models.IntegerField()
