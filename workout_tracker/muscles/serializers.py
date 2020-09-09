from rest_framework import serializers
from .models import MuscleSubportion, Muscle, MuscleGrouping


class MuscleSubportionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleSubportion
        fields = ['name']


class MuscleSerializer(serializers.ModelSerializer):
    sub = MuscleSubportionSerializer(source='subportions', many=True)

    class Meta:
        model = Muscle
        fields = ['name', 'sub']


class MuscleGroupingSerializer(serializers.ModelSerializer):
    sub = MuscleSerializer(source='muscles', many=True)

    class Meta:
        model = MuscleGrouping
        fields = ['name', 'snames', 'sub']
