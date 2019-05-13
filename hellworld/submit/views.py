import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from submit.models import Task, Submit
from submit.serializers import SubmitCreateSerializer


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
        ), ContentFile(code.encode('utf-8')))
        submit.save()

        transaction.on_commit(lambda: submit.run_scoring())

        return JsonResponse(
            {'id': submit.pk, 'task_name': submit.task.name, 'status': submit.get_status_display()}
        )


class SubmitListView(AuthorizedApiView):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        qs = Submit.objects.select_related('task').filter(participant=request.user).order_by('id')
        data = []
        for submit in qs:
            submit_data = {
                'task_name': submit.task.name,
                'status': submit.get_status_display(),
                'id': submit.id,
            }
            data.append(submit_data)
        return JsonResponse(data, safe=False)


class SubmitStatusRequestView(AuthorizedApiView):

    @transaction.atomic
    def get(self, request, submit_pk, *args, **kwargs):
        submit = Submit.objects.get(pk=submit_pk)

        if request.user != submit.participant:
            return HttpResponseForbidden()

        return JsonResponse({
            'id': submit.id,
            'task_id': submit.task_id,
            'status_code': submit.status,
            'status': submit.get_status_display()
        })


class TaskListView(AuthorizedApiView):
    def get(self, request, *args, **kwargs):
        qs = Task.objects.all().order_by('name')
        return JsonResponse([
            {
                'id': task.id,
                'name': task.name,
                'points': task.max_points,
                'is_solved': Submit.objects.select_related('task').filter(task=task, status=Submit.STATUS_OK, participant=request.user).exists()
            } for task in qs
        ], safe=False)


class LanguageListView(AuthorizedApiView):
    def get(self, request, *args, **kwargs):
        return JsonResponse([{'id': language[0], 'name': language[1]} for language in Submit.LANGUAGE_CHOICES], safe=False)


class TaskAssignmentAPIView(AuthorizedApiView):

    def get(self, request, task_pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=task_pk)
        if not task.assignment:
            return Http404()

        response = HttpResponse(task.assignment, content_type='application/pdf')
        return response
