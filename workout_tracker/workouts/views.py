from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
from core.permissions import IsAdmin, IsOwner
from core.views import ListRetrieveUpdateDestroyViewSet

from .models import WorkoutTemplate, Workout
from .serializers import WorkoutTemplateSerializer, WorkoutSerializer


class WorkoutTemplateViewSet(ListRetrieveUpdateDestroyViewSet):
    queryset = WorkoutTemplate.objects.all()
    serializer_class = WorkoutTemplateSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdmin | IsOwner]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], url_path='create-workout')
    def create_workout(self, request, pk=None):
        workout_template = self.get_object()
        workout = workout_template.create_workout()
        serializer = WorkoutSerializer(workout, context={'request': request})
        return Response(data=serializer.data)


class UserWorkoutTemplateViewSet(ListCreateAPIView):
    serializer_class = WorkoutTemplateSerializer
    permission_classes = [IsAdmin | IsOwner]

    def get_queryset(self):
        return WorkoutTemplate.objects.filter(owner=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(owner=get_user_model().objects.get(pk=self.kwargs['pk']))


class WorkoutViewSet(ListRetrieveUpdateDestroyViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdmin | IsOwner]

        return [permission() for permission in permission_classes]
