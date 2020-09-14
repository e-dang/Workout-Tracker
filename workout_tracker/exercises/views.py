from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView

from core.permissions import IsAdmin, IsOwner
from core.views import ListRetrieveUpdateDestroyViewSet

from .filters import ExerciseTemplateFilterSet
from .models import ExerciseTemplate
from .serializers import ExerciseTemplateSerializer


class ExerciseTemplateViewSet(ListRetrieveUpdateDestroyViewSet):
    queryset = ExerciseTemplate.objects.all()
    serializer_class = ExerciseTemplateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExerciseTemplateFilterSet
    search_fields = ['owner__username', 'name', 'snames', 'created']
    ordering_fields = ['owner__username', 'name', 'created']
    ordering = ['owner__username', 'name']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdmin | IsOwner]

        return [permission() for permission in permission_classes]


class UserExerciseTemplateViewSet(ListCreateAPIView):
    serializer_class = ExerciseTemplateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExerciseTemplateFilterSet
    search_fields = ['name', 'snames', 'created']
    ordering_fields = ['name', 'created']
    ordering = ['name']
    permission_classes = [IsAdmin | IsOwner]

    def get_queryset(self):
        return ExerciseTemplate.objects.filter(owner=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(owner=get_user_model().objects.get(pk=self.kwargs['pk']))
