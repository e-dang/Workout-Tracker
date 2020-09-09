from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import MuscleGroupingFilter
from .models import MuscleGrouping
from .serializers import MuscleGroupingSerializer


class MuscleGroupingViewSet(ReadOnlyModelViewSet):
    queryset = MuscleGrouping.objects.all()
    serializer_class = MuscleGroupingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MuscleGroupingFilter
    search_fields = ['name', 'snames', 'muscles__name', 'muscles__subportions__name']
    ordering_fields = ['name']
    ordering = ['name']
