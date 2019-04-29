from django.db import transaction
from django.views.generic import TemplateView

from pandemic.models import DiseaseClass, DiseaseInstance
from people.models import Team


class DiseaseBalance(TemplateView):
    template_name = 'pandemic/balance.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'diseases': [x for x in DiseaseClass.objects.order_by('name')]
        })
        return data

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if kwargs.get('disease_pk', None):
            disease = DiseaseClass.objects.get(pk=kwargs['disease_pk'])
            instances = DiseaseInstance.objects.filter(disease=disease)
            for ins in instances:
                ins.severity = ins.severity + int(request.POST.get('severity', 0))
                ins.effect_duration = ins.effect_duration + int(request.POST.get('effect', 0))
                ins.cooldown_duration = ins.cooldown_duration + int(request.POST.get('cooldown', 0))
                ins.save()
        return self.get(request, *args, **kwargs)


class ResourceView(TemplateView):
    template_name = 'pandemic/resources.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'teams': [team for team in Team.objects.order_by('name')]
        })
        return data

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if kwargs.get('team_pk', None):
            resource = request.POST.get('resource', 0)
            team = Team.objects.get(pk=kwargs['team_pk'])
            team.resources = team.resources + int(resource)
            team.save()
        return self.get(request, *args, **kwargs)
