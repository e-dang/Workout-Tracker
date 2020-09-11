from .models import Movement
from core.serializers import OwnedMultiAliasResourceSerializer, extend_fields


class MovementSerializer(OwnedMultiAliasResourceSerializer):
    class Meta:
        model = Movement
        fields = extend_fields(OwnedMultiAliasResourceSerializer, ['muscles', 'equipment'])
        extra_kwargs = {
            'muscles': {'view_name': 'muscle-detail', 'lookup_field': 'pk'}
        }
