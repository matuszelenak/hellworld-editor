from rest_framework import serializers

from submit.models import Submit


class SubmitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submit
        fields = ('file', 'language', 'task')
