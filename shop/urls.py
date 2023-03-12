from django.urls import path
from .views import (
    ShopDetailView,
    create_shop_contact,
    ShopProductsView,
    ShopListView,
    register_shop,
    register_shop_seller_information_create,
    register_shop_create,

    # panel
    ShopAccountMainView,
    ShopProductsListView,
    ShopProductUpdateView,
    ShopProductCreateView,
    ShopOrderListView,
    ShopOrderDetailView,
    ShopOrderUpdateView
)

app_name = 'shop'
urlpatterns = [
    path('shops/register-shop/', register_shop, name='register-shop'),
    path('shops/', ShopListView.as_view(), name='shop-list'),
    path('<slug>', ShopDetailView.as_view(), name='shop-detail'),
    path('<slug>/contact', create_shop_contact, name='shop-contact'),
    path('<slug>/products', ShopProductsView.as_view(), name='shop-products'),

    # ajax urls
    path(
        'shops/register-shop/seller-information-create',
        register_shop_seller_information_create,
        name='seller-information-create'
    ),
    path(
        'shops/register-shop/data-create',
        register_shop_create,
        name='shop-data-create'
    ),

    # panel
    path('shop/panel/<unique_uuid>', ShopAccountMainView.as_view(), name='shop-panel-main'),

    path(
        'shop/panel/<unique_uuid>/products',
        ShopProductsListView.as_view(),
        name='shop-panel-products'
    ),
    path(
        'shop/panel/<unique_uuid>/products/update/<str:pk>',
        ShopProductUpdateView.as_view(),
        name='shop-panel-products-update'
    ),
    path(
        'shop/panel/<unique_uuid>/products/create',
        ShopProductCreateView.as_view(),
        name='shop-panel-products-create'
    ),

    path(
        'shop/panel/<unique_uuid>/orders',
        ShopOrderListView.as_view(),
        name='shop-panel-orders'
    ),
    path(
        'shop/panel/<unique_uuid>/orders/<int:pk>',
        ShopOrderDetailView.as_view(),
        name='shop-panel-orders-detail'
    ),
    path(
        'shop/panel/<unique_uuid>/orders/update/<int:pk>',
        ShopOrderUpdateView.as_view(),
        name='shop-panel-orders-update'
    )
]
