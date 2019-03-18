from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from rest_framework.response import Response

from rest_framework.views import APIView

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
        submit = serializer.create(data)

        transaction.on_commit(lambda: submit.run_scoring())

        return Response(data={'status': 'OK'})
