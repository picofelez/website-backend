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
    sort_by = django_filters.CharFilter(method='sort_query')

    def search_query(self, queryset, search, value):
        lookup = (
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(keywords__icontains=value)
        )
        return queryset.filter(lookup)

    def sort_query(self, queryset, sort_by, value):
        if value == '-time':
            return queryset.order_by('-created')
        elif value == '-hits':
            return queryset
        elif value == 'price':
            return queryset.filter(stock__gt=1).order_by('price')
        elif value == '-price':
            return queryset.filter(stock__gt=1).order_by('-price')
        return queryset

    class Meta:
        model = Product
        fields = ('shop', 'title', 'description', 'keywords', 'price', 'categories', 'purchase_limit')
