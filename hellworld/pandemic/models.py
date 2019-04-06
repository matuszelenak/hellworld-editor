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

    def __str__(self):
        return self.name


class DiseaseInstance(models.Model):
    disease = models.ForeignKey('pandemic.DiseaseClass', related_name='instances', on_delete=models.CASCADE)
    participant = models.ForeignKey('people.Participant', related_name='diseases', on_delete=models.CASCADE)

    effect_duration = models.IntegerField(default=5)
    cooldown_duration = models.IntegerField(default=60)
    severity = models.IntegerField(null=False, default=1)

    def __str__(self):
        return f'{str(self.disease)} on {str(self.participant)}'


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
