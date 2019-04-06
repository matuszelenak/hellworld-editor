from rest_framework import serializers

from pandemic.models import DiseaseInstance


class DiseaseInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiseaseInstance
        fields = ('severity', 'disease', 'effect_duration', 'cooldown_duration')
        depth = 2
