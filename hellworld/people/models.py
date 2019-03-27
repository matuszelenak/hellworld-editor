from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser


class Team(models.Model):
    name = models.CharField(max_length=40, null=False)
    logged_in = models.OneToOneField('people.Participant', on_delete=models.SET_NULL, null=True, related_name='+')


class Participant(AbstractUser):
    team = models.ForeignKey('people.Team', related_name='members', on_delete=models.SET_NULL, null=True, blank=True)
    is_organiser = models.BooleanField(default=False)


class BluetoothTag(models.Model):
    address = models.TextField(null=False)
    team = models.ForeignKey('people.Team', related_name='tags', on_delete=models.CASCADE)


class MedicineSupply(models.Model):
    participant = models.ForeignKey('people.Participant', related_name='medicine_supplies', on_delete=models.CASCADE)
    medicine = models.ForeignKey('pandemic.MedicineClass', related_name='participant_supplies', on_delete=models.CASCADE)
