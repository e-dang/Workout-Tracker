from django.contrib.postgres.fields import ArrayField
from django_filters import rest_framework as filters

from .models import MuscleGrouping


class MuscleGroupingFilter(filters.FilterSet):
    class Meta:
        model = MuscleGrouping
        fields = {
            'name': ['iexact'],
            'snames': ['icontains'],
            'muscles__name': ['iexact'],
            'muscles__subportions__name': ['iexact']
        }
        filter_overrides = {
            ArrayField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
