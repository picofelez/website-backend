from django.urls import path
from .views import (
    ProductDetailView,
    ProductListView,
    MultipleProductDetailView
)

app_name = 'product'
urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    # path('<pk>', ProductDetailView.as_view(), name='product-detail'),
    path('multiple/<pk>', MultipleProductDetailView.as_view(), name='multiple-product-detail')
]
