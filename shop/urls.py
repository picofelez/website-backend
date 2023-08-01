from django.urls import path
from .views import (
    ShopDetailView,
    create_shop_contact,
    ShopProductsView,
    ShopRatingView,

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
    ShopOrderUpdateView,
    ShopUpdateView,
    shop_wallet_view,
    ShopUpdateProductPriceView,
    ShopInvoiceListListView,
    ShopInvoiceDetailDetailView,
    create_shop_invoice_view,
    update_shop_invoice_view,
    customer_for_invoice_ajax_view
)

app_name = 'shop'
urlpatterns = [
    path('shops/register-shop/', register_shop, name='register-shop'),
    path('shops/', ShopListView.as_view(), name='shop-list'),
    path('<slug>', ShopDetailView.as_view(), name='shop-detail'),
    path('<slug>/contact', create_shop_contact, name='shop-contact'),
    path('<slug>/products', ShopProductsView.as_view(), name='shop-products'),
    path('<slug>/rating', ShopRatingView.as_view(), name='shop-rating'),

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
    path('shop/panel/<unique_uuid>/update', ShopUpdateView.as_view(), name='shop-panel-update'),
    # path('shop/panel/<unique_uuid>/wallet', shop_wallet_view, name='shop-panel-wallet'),

    # path(
    #     'shop/panel/<unique_uuid>/products',
    #     ShopProductsListView.as_view(),
    #     name='shop-panel-products'
    # ),
    # path(
    #     'shop/panel/<unique_uuid>/products/update/<str:pk>',
    #     ShopProductUpdateView.as_view(),
    #     name='shop-panel-products-update'
    # ),
    # path(
    #     'shop/panel/<unique_uuid>/products/update/price/<str:pk>',
    #     ShopUpdateProductPriceView.as_view(),
    #     name='shop-panel-products-update-price'
    # ),
    # path(
    #     'shop/panel/<unique_uuid>/products/create',
    #     ShopProductCreateView.as_view(),
    #     name='shop-panel-products-create'
    # ),

    # path(
    #     'shop/panel/<unique_uuid>/orders',
    #     ShopOrderListView.as_view(),
    #     name='shop-panel-orders'
    # ),
    # path(
    #     'shop/panel/<unique_uuid>/orders/<int:pk>',
    #     ShopOrderDetailView.as_view(),
    #     name='shop-panel-orders-detail'
    # ),
    # path(
    #     'shop/panel/<unique_uuid>/orders/update/<int:pk>',
    #     ShopOrderUpdateView.as_view(),
    #     name='shop-panel-orders-update'
    # ),

    # special shops
    path(
        'shop/panel/<unique_uuid>/invoices',
        ShopInvoiceListListView.as_view(),
        name='shop-panel-invoices'
    ),
    path(
        'shop/panel/<unique_uuid>/invoices/create',
        create_shop_invoice_view,
        name='shop-panel-invoices-create'
    ),
    path(
        'shop/panel/<unique_uuid>/invoices/create/customer',
        customer_for_invoice_ajax_view,
        name='shop-panel-invoices-create-customer'
    ),
    path(
        'shop/panel/<unique_uuid>/invoices/update/<str:pk>',
        update_shop_invoice_view,
        name='shop-panel-invoices-update'
    ),
    path(
        'shop/panel/<unique_uuid>/invoices/<str:pk>',
        ShopInvoiceDetailDetailView.as_view(),
        name='shop-panel-invoices-detail'
    ),
]
