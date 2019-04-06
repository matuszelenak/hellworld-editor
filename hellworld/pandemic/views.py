import json
import os
import random

from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from hellworld import settings
from pandemic.models import DiseaseInstance, DiseaseTransmit, DiseaseClass, MedicineClass, MedicineEffect
from pandemic.serializers import DiseaseInstanceSerializer
from people.models import BluetoothTag, Team, MedicineSupply
from submit.models import Submit, Task
from submit.views import AuthorizedApiView


class EditorView(TemplateView):
    template_name = "pandemic/editor.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(
            {
                'submit_cls': Submit,
                'tasks': [
                    {
                        'name': task.name,
                        'pk': task.pk,
                        'points': task.max_points
                    }
                    for task in Task.objects.order_by('name')
                ],
                'balance': self.request.user.team.resources
            }
        )
        return data


class CompetitionRules(View):
    def get(self, request, *args, **kwargs):

        data = {
            'languages': {
                k: v for v, k in Submit.LANGUAGE_CHOICES
            },
            'submit_statuses': {
                k: v for k, v in Submit.STATUS_CHOICES
            },
            'diseases': [
                {
                    'name': x.name,
                    'description': x.description
                }
                for x in DiseaseClass.objects.all()
            ]
        }

        return JsonResponse(data)


class ActiveDiseaseInstancesView(View):
    def get(self, request, *args, **kwargs):
        instances = DiseaseInstance.objects.select_related('disease', 'team').filter(team=request.user.team)
        serializer = DiseaseInstanceSerializer(instances, many=True)

        return JsonResponse(serializer.data, safe=False)


class BluetoothTagSubmitView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        content = json.loads(request.body)
        if not ('address' in content and 'target' in content):
            return HttpResponseBadRequest()

        tag = BluetoothTag.objects.select_for_update().filter(address=content['address']).first()
        if not tag:
            raise Http404()
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
        print(request.body)
        data = json.loads(request.body)
        medicine = MedicineClass.objects.get(pk=data['medicine_pk'])
        supply = MedicineSupply.objects.filter(team=team, medicine=medicine, amount__gt=0).first()
        if not supply:
            return JsonResponse({'message': 'You do not have anymore'})

        for medicine_effect in MedicineEffect.objects.filter(medicine=medicine):
            print(medicine_effect)
            for inst in DiseaseInstance.objects.filter(team=team, disease=medicine_effect.disease):
                print(inst)
                inst.cooldown_duration = inst.cooldown_duration * medicine_effect.cooldown_multiplier
                inst.effect_duration = inst.effect_duration * medicine_effect.effect_multiplier
                inst.severity = inst.severity * medicine_effect.severity_multiplier
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


class ADHDPagesView(View):
    def get(self, request, *args, **kwargs):
        img_dir = os.path.join(settings.MEDIA_ROOT, 'adhd_screenshots')
        img = random.choice(os.listdir(img_dir))
        image_data = open(os.path.join(img_dir, img), "rb").read()
        return HttpResponse(image_data, content_type="image/png")


class YawnView(View):
    def get(self, request, *args, **kwargs):
        fname = os.path.join(settings.MEDIA_ROOT, 'sounds', 'yawn.mp3')
        f = open(fname, "rb")
        response = HttpResponse()
        response.write(f.read())
        response['Content-Type'] = 'audio/mp3'
        response['Content-Length'] = os.path.getsize(fname)
        return response
