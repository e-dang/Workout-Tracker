from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from core.views import ListRetrieveUpdateDestroyViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(ListRetrieveUpdateDestroyViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['username', 'first_name', 'last_name']
    ordering = ['username']

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
