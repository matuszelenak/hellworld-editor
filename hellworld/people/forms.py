from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Participant


class ParticipantCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Participant
        fields = ('username', 'email', 'is_organiser', 'team')


class ParticipantChangeForm(UserChangeForm):

    class Meta:
        model = Participant
        fields = ('username', 'email', 'is_organiser', 'team')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
