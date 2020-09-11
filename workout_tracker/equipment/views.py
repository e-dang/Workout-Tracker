from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView

from core.permissions import IsAdmin, IsOwner
from core.views import ListRetrieveUpdateDeleteViewSet

from .filters import EquipmentFilterSet
from .models import Equipment
from .serializers import EquipmentSerializer


class EquipmentViewSet(ListRetrieveUpdateDeleteViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EquipmentFilterSet
    search_fields = ['owner', 'name', 'snames', 'created']
    ordering_fields = ['owner', 'name', 'created']
    ordering = ['owner', 'name']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdmin | IsOwner]

        return [permission() for permission in permission_classes]


class UserEquipmentListCreateView(ListCreateAPIView):
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EquipmentFilterSet
    search_fields = ['name', 'snames', 'created']
    ordering_fields = ['name', 'created']
    ordering = ['name']
    permission_classes = [IsAdmin | IsOwner]

    def get_queryset(self):
        return Equipment.objects.filter(owner=self.kwargs['pk'])

    def perform_create(self, serializer):
        owner_model = ContentType.objects.get(model=settings.AUTH_USER_MODEL).model_class()
        serializer.save(owner=owner_model.objects.get(self.kwargs['pk']))
