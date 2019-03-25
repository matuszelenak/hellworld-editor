from django.contrib import admin

from people.forms import ParticipantChangeForm, ParticipantCreationForm
from people.models import Participant, Team


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    add_form = ParticipantCreationForm
    form = ParticipantChangeForm
    model = Participant
    list_display = ['email', 'username']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass
