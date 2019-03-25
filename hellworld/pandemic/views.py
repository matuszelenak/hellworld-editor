from django.http import JsonResponse
from django.views.generic import TemplateView

from pandemic.models import DiseaseInstance
from pandemic.serializers import DiseaseInstanceSerializer
from submit.views import AuthorizedApiView


class EditorView(TemplateView):
    template_name = "pandemic/editor.html"


class ActiveDiseaseInstancesView(AuthorizedApiView):
    def get(self, request, *args, **kwargs):
        instances = DiseaseInstance.objects.select_related('disease', 'participant').filter(participant=request.user)
        serializer = DiseaseInstanceSerializer(instances, many=True)

        return JsonResponse(serializer.data)
