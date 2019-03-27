import json

from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from pandemic.models import DiseaseInstance, DiseaseTransmit
from pandemic.serializers import DiseaseInstanceSerializer
from people.models import BluetoothTag, Team
from submit.views import AuthorizedApiView


class EditorView(TemplateView):
    template_name = "pandemic/editor.html"


class ActiveDiseaseInstancesView(AuthorizedApiView):
    def get(self, request, *args, **kwargs):
        instances = DiseaseInstance.objects.select_related('disease', 'participant').filter(participant=request.user)
        serializer = DiseaseInstanceSerializer(instances, many=True)

        return JsonResponse(serializer.data)


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

        participant = target_team.logged_in
        if participant:
            transmits = DiseaseTransmit.objects.filter(tag=tag)
            existing_instances = DiseaseInstance.objects.filter(participant=participant)
            for transmit in transmits:
                instance = existing_instances.filter(disease=transmit.disease)

                if instance.exists():
                    instance.update(severity=max(instance.first().severity, transmit.severity))
                else:
                    DiseaseInstance.objects.create(
                        disease=transmit.disease,
                        participant=participant,
                        severity=transmit.severity
                    )

            transmits.delete()
            return JsonResponse({'result': 'infected'})
        else:
            return JsonResponse({'result': 'dodged'})

