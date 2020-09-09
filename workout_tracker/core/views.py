from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


class ListRetrieveUpdateDeleteViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin,
                                      GenericViewSet):
    pass
