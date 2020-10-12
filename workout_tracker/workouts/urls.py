from rest_framework.routers import DefaultRouter

from .views import WorkoutTemplateViewSet, WorkoutViewSet

router = DefaultRouter()
router.register(r'templates', WorkoutTemplateViewSet, basename='workout-template')
router.register(r'', WorkoutViewSet, basename='workout')

urlpatterns = router.urls
