from django.http import JsonResponse
from django.templatetags.static import static
from django.views import View

from pandemic.models import DiseaseInstance
from pandemic.serializers import DiseaseInstanceSerializer


class ActiveDiseaseInstancesView(View):
    def get(self, request, *args, **kwargs):
        instances = DiseaseInstance.objects.select_related('disease', 'team').filter(team=request.user.team, severity__gt=0).order_by('disease__name')
        serializer = DiseaseInstanceSerializer(instances, many=True)

        return JsonResponse(serializer.data, safe=False)


class ADHDImagesPaths(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse([static(f'pandemic/img/adhd{i}.png') for i in range(1, 10)], safe=False)
