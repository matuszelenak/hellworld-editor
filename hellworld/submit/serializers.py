from rest_framework import serializers

from submit.models import Submit


class SubmitCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=10000, allow_blank=True)

    def create(self, validated_data):
        validated_data.pop('code')
        return Submit(
            **validated_data
        )

    class Meta:
        model = Submit
        fields = ('code', 'language', 'task')


class SubmitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submit
        fields = ('participant', 'task', 'status',)
        depth = 2
