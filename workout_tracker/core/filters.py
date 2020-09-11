from django_filters import rest_framework as filters


class MultiAliasResourceFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='iexact')
    snames = filters.CharFilter(method='filter_snames')
    created = filters.DateTimeFilter()

    def filter_snames(self, queryset, name, value):
        lookup = '__'.join([name, 'icontains'])
        return queryset.filter(**{lookup: value})


class OwnedMultiAliasResourceFilterSet(MultiAliasResourceFilterSet):
    owner = filters.NumberFilter(field_name='owner__id', lookup_expr='exact')
    owner__username = filters.CharFilter(field_name='owner__username', lookup_expr='iexact')
    owner__first_name = filters.CharFilter(field_name='owner__first_name', lookup_expr='iexact')
    owner__last_name = filters.CharFilter(field_name='owner__last_name', lookup_expr='iexact')
