from rest_framework.routers import DefaultRouter
from .views import MovementViewSet

router = DefaultRouter()
router.register(r'', MovementViewSet)

urlpatterns = router.urls
