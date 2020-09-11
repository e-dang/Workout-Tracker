from core.filters import OwnedMultiAliasResourceFilterSet
from .models import Movement


class MovementFilter(OwnedMultiAliasResourceFilterSet):
    class Meta:
        model = Movement
        fields = ['equipment', 'muscles', 'description']
