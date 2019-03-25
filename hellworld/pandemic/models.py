from django.db import models


class DiseaseClass(models.Model):
    TYPE_INFECTIOUS = 0
    TYPE_DEGENERATIVE = 1

    TYPES = (
        (TYPE_INFECTIOUS, 'Infectious'),
        (TYPE_DEGENERATIVE, 'Degenerative')
    )

    name = models.TextField(null=False)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES)


class DiseaseInstance(models.Model):
    disease = models.ForeignKey('pandemic.DiseaseClass', related_name='instances', on_delete=models.CASCADE)
    participant = models.ForeignKey('people.Participant', related_name='diseases', on_delete=models.CASCADE)
    severity = models.IntegerField(null=False, default=1)


class DiseaseTransmit(models.Model):
    disease = models.ForeignKey('pandemic.DiseaseClass', related_name='transmissions', on_delete=models.CASCADE)
    tag = models.ForeignKey('people.BluetoothTag', related_name='transmissions', on_delete=models.CASCADE)
    severity = models.IntegerField(null=False)


class MedicineClass(models.Model):
    name = models.TextField(null=False)
    description = models.TextField()


class MedicineEffect(models.Model):
    medicine = models.ForeignKey('pandemic.MedicineClass', related_name='applications', on_delete=models.CASCADE)
    disease = models.ForeignKey('pandemic.DiseaseClass', related_name='applied_medicines', on_delete=models.CASCADE)
    strength = models.IntegerField()
