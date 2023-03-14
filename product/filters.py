import django_filters
from django import forms
from django.db.models import Q

from product.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    title = django_filters.CharFilter(lookup_expr='icontains')
    search = django_filters.CharFilter(method='search_query')

    def search_query(self, queryset, search, value):
        lookup = (
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(keywords__icontains=value)
        )
        return queryset.filter(lookup)

    class Meta:
        model = Product
        fields = ('shop', 'title', 'description', 'keywords', 'price', 'categories', 'purchase_limit')
