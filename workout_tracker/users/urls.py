from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from equipment.views import UserEquipmentListCreateView
from movements.views import UserMovementListCreateView
from exercises.views import UserExerciseTemplateViewSet
from workouts.views import UserWorkoutTemplateViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('<int:pk>/equipment/', UserEquipmentListCreateView.as_view(), name='user-equipment-list'),
    path('<int:pk>/movements/', UserMovementListCreateView.as_view(), name='user-movement-list'),
    path('<int:pk>/exercises/', UserExerciseTemplateViewSet.as_view(), name='user-exercise-list'),
    path('<int:pk>/workouts/templates/', UserWorkoutTemplateViewSet.as_view(), name='user-workout-templates-list')
]
urlpatterns += router.urls
