from rest_framework import serializers
from .models import MultiAliasResource, OwnedMultiAliasResource
from .utils import extend_fields
from users.serializers import UserSerializer


class MultiAliasedResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MultiAliasResource
        fields = ['url', 'id', 'name', 'snames', 'created']
        abstract = True


class OwnedMultiAliasResourceSerializer(MultiAliasedResourceSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = OwnedMultiAliasResource
        fields = extend_fields(MultiAliasedResourceSerializer, ['owner'])
        abstract = True
