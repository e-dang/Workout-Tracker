from rest_framework import serializers
from .models import MuscleSubportion, Muscle, MuscleGrouping


class MuscleSubportionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MuscleSubportion
        fields = ['name']


class MuscleSerializer(serializers.HyperlinkedModelSerializer):
    sub = MuscleSubportionSerializer(source='subportions', many=True)

    class Meta:
        model = Muscle
        fields = ['name', 'sub']


class MuscleGroupingSerializer(serializers.HyperlinkedModelSerializer):
    sub = MuscleSerializer(source='muscles', many=True)

    class Meta:
        model = MuscleGrouping
        fields = ['url', 'name', 'snames', 'sub']
        extra_kwargs = {
            'url': {'view_name': 'muscle-detail', 'lookup_field': 'pk'}
        }
