import django_filters
from django.db.models import Q

from metallurgy.models import WorkSample


class WorkSampleFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_query')

    def search_query(self, queryset, search, value):
        lookup = (
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(address__icontains=value) |
                Q(date__icontains=value)
        )
        return queryset.filter(lookup)

    class Meta:
        model = WorkSample
        fields = ('title', 'description', 'address', 'date')
