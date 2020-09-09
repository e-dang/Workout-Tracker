from rest_framework.routers import DefaultRouter
from .views import MuscleGroupingViewSet

router = DefaultRouter()
router.register(r'', MuscleGroupingViewSet, basename='muscle')

urlpatterns = router.urls
