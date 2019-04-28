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
    team = models.ForeignKey('people.Team', related_name='diseases', on_delete=models.CASCADE)

    effect_duration = models.IntegerField(default=5)
    cooldown_duration = models.IntegerField(default=60)
    severity = models.IntegerField(null=False, default=1)

    def __str__(self):
        return f'{str(self.disease)} on {str(self.team)}'


class DiseaseTransmit(models.Model):
    disease = models.ForeignKey('pandemic.DiseaseClass', related_name='transmissions', on_delete=models.CASCADE)
    tag = models.ForeignKey('people.BluetoothTag', related_name='transmissions', on_delete=models.CASCADE, null=True)
    severity = models.IntegerField(null=False)

    def __str__(self):
        return f'{str(self.tag)} carries {str(self.disease)}'


class MedicineClass(models.Model):
    price = models.IntegerField(default=5)
    name = models.TextField(null=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class MedicineEffect(models.Model):
    medicine = models.ForeignKey('pandemic.MedicineClass', related_name='applications', on_delete=models.CASCADE)
    disease = models.ForeignKey('pandemic.DiseaseClass', related_name='applied_medicines', on_delete=models.CASCADE)

    severity_multiplier = models.FloatField(default=0.5)
    effect_multiplier = models.FloatField(default=0.5)
    cooldown_multiplier = models.FloatField(default=2)

    def __str__(self):
        return str(self.medicine) + ' works on ' + str(self.disease)