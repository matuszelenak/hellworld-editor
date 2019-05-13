import json
import math

from django.db import transaction
from django.http import HttpResponseBadRequest, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from pandemic.models import DiseaseTransmit, DiseaseInstance, MedicineEffect, MedicineClass
from people.models import Team, BluetoothTag, MedicineSupply


class EditorView(TemplateView):
    template_name = "pandemic/editor.html"


class PurchaseMedicine(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        team = request.user.team
        data = json.loads(request.body)
        medicine = MedicineClass.objects.get(pk=data['medicine_pk'])
        supply = MedicineSupply.objects.filter(team=team, medicine=medicine).first()
        if team.resources >= medicine.price:
            team.resources -= medicine.price
            team.save()

            supply.amount += 1
            supply.save()
            return JsonResponse({'message': 'Purchase successful', 'balance': team.resources})
        return JsonResponse({'message': 'Not enough funds', 'balance': team.resources})


class MedicineInventory(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        team = request.user.team
        data = json.loads(request.body)
        medicine = MedicineClass.objects.get(pk=data['medicine_pk'])
        supply = MedicineSupply.objects.filter(team=team, medicine=medicine, amount__gt=0).first()
        if not supply:
            return JsonResponse({'message': 'You do not have anymore'})

        for medicine_effect in MedicineEffect.objects.filter(medicine=medicine):
            for inst in DiseaseInstance.objects.filter(team=team, disease=medicine_effect.disease):
                inst.cooldown_duration = math.ceil(inst.cooldown_duration * medicine_effect.cooldown_multiplier)
                inst.effect_duration = math.ceil(inst.effect_duration * medicine_effect.effect_multiplier)
                inst.severity = math.ceil(inst.severity * medicine_effect.severity_multiplier)
                inst.save()

        supply.amount -= 1
        supply.save()

        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        team = request.user.team
        supplies = MedicineSupply.objects.filter(team=team)
        return JsonResponse(
            [
                {
                    'amount': s.amount,
                    'medicine_name': s.medicine.name,
                    'medicine_pk': s.medicine.pk,
                    'price': s.medicine.price,
                    'description': s.medicine.description
                }
                for s in supplies
            ], safe=False
        )


class BluetoothTagSubmitView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        content = json.loads(request.body)
        if not ('address' in content and 'target' in content):
            return HttpResponseBadRequest()

        tag = get_object_or_404(BluetoothTag, address=content['address'])
        target_team = get_object_or_404(Team, pk=content['target'])

        transmits = DiseaseTransmit.objects.filter(tag=tag)
        existing_instances = DiseaseInstance.objects.filter(team=target_team)
        for transmit in transmits:
            instance = existing_instances.filter(disease=transmit.disease)

            if instance.exists():
                instance.update(severity=max(instance.first().severity, transmit.severity))
            else:
                DiseaseInstance.objects.create(
                    disease=transmit.disease,
                    team=target_team,
                    severity=transmit.severity
                )

        transmits.delete()
        return JsonResponse({'result': 'infected'})
