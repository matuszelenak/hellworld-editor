from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.TextField(null=False)


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey('people.Team', related_name='members', on_delete=models.SET_NULL, null=True)


class BluetoothTag(models.Model):
    address = models.TextField(null=False)
    team_id = models.ForeignKey('people.Team', related_name='tags', on_delete=models.CASCADE)


class MedicineSupply(models.Model):
    participant_id = models.ForeignKey('people.Participant', related_name='medicine_suppplies', on_delete=models.CASCADE)
    medicine_id = models.ForeignKey('pandemic.MedicineClass', related_name='participant_supplies', on_delete=models.CASCADE)
