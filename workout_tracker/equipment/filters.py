from django.contrib.postgres.fields import ArrayField
from django_filters import rest_framework as filters

from .models import Equipment


class EquipmentFilter(filters.FilterSet):
    class Meta:
        model = Equipment
        fields = {
            'name': ['iexact'],
            'snames': ['icontains'],
            'owner__username': ['iexact'],
            'owner__first_name': ['iexact'],
            'owner__last_name': ['iexact']
        }
        filter_overrides = {
            ArrayField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
