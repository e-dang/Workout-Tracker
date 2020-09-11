from .models import Equipment

from core.serializers import OwnedMultiAliasResourceSerializer


class EquipmentSerializer(OwnedMultiAliasResourceSerializer):
    class Meta:
        model = Equipment
        fields = OwnedMultiAliasResourceSerializer.Meta.fields
