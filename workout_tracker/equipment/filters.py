from core.filters import OwnedMultiAliasResourceFilterSet

from .models import Equipment


class EquipmentFilterSet(OwnedMultiAliasResourceFilterSet):
    class Meta:
        model = Equipment
        fields = []
