import django_filters
from django import forms

from product.models import Product, Category


class ProductFilter(django_filters.FilterSet):
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('shop', 'title', 'description', 'keywords', 'price', 'categories', 'purchase_limit')
