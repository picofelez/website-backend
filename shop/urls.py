from django.urls import path
from .views import (
    ShopDetailView,
    create_shop_contact, ShopProductsView
)

app_name = 'shop'
urlpatterns = [
    path('<slug>', ShopDetailView.as_view(), name='shop-detail'),
    path('<slug>/contact', create_shop_contact, name='shop-contact'),
    path('<slug>/products', ShopProductsView.as_view(), name='shop-products'),
]
