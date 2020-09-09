from rest_framework import serializers
from .models import Equipment


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipment
        fields = ['url', 'id', 'name', 'snames', 'owner']
        read_only_fields = ['url', 'id', 'owner']
