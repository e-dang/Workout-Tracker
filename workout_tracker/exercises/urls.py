from rest_framework.routers import DefaultRouter

from .views import ExerciseTemplateViewSet

router = DefaultRouter()
router.register(r'', ExerciseTemplateViewSet, basename='exercise')

urlpatterns = router.urls
