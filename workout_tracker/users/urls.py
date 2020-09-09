from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from equipment.views import UserEquipmentListCreateView

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('<int:pk>/equipment/', UserEquipmentListCreateView.as_view(), name='user-equipment-list')
]
urlpatterns += router.urls
