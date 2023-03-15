import django_filters
from django.db.models import Q

from .models import Article


class ArticleFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_query')

    def search_query(self, queryset, search, value):
        lookup = (
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(summary__icontains=value)
        )
        return queryset.filter(lookup)

    class Meta:
        model = Article
        fields = ('title', 'tags')
