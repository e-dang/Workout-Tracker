from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class ListRetrieveUpdateDestroyViewSet(mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       GenericViewSet):
    pass
