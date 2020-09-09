from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from core.views import ListRetrieveUpdateDeleteViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(ListRetrieveUpdateDeleteViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['username', 'first_name', 'last_name']
    ordering = ['username']

    def perform_destory(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=HTTP_204_NO_CONTENT)
