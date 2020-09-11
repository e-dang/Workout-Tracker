from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from equipment.views import UserEquipmentListCreateView
from movements.views import UserMovementListCreateView

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('<int:pk>/equipment/', UserEquipmentListCreateView.as_view(), name='user-equipment-list'),
    path('<int:pk>/movements/', UserMovementListCreateView.as_view(), name='user-movement-list')
]
urlpatterns += router.urls
