import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from submit.models import Task, Submit
from submit.serializers import SubmitCreateSerializer, SubmitSerializer


class AuthorizedApiView(LoginRequiredMixin, APIView):
    pass


class CodeSubmitAPIView(AuthorizedApiView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = SubmitCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['participant'] = request.user
        code = data['code']
        submit = serializer.create(data)

        submit.file.save('{id}{ext}'.format(
            id=str(uuid.uuid4()),
            ext=Submit.LANGUAGE_EXTENSIONS[submit.language]
        ), ContentFile(code))
        submit.save()

        transaction.on_commit(lambda: submit.run_scoring())

        return JsonResponse(
            {'submit_id': submit.pk}
        )


class SubmitStatusRequestView(AuthorizedApiView):

    def get(self, request, submit_pk, *args, **kwargs):
        submit = Submit.objects.get(pk=submit_pk)

        if request.user != submit.participant:
            return HttpResponseForbidden()

        serializer = SubmitSerializer(instance=submit)
        return JsonResponse(serializer.data)


class TaskAssignmentAPIView(AuthorizedApiView):

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['task_pk'])
        if not task.assignment:
            return Http404()

        response = HttpResponse(task.assignment, content_type='application/pdf')

        return response
