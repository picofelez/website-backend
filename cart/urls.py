from django.urls import path
from .views import (
    cart_add_view,
    cart_remove_view,
    CartListView
)

app_name = 'cart'
urlpatterns = [
    path('', CartListView.as_view(), name='cart-list'),

    path('add/<str:product_id>', cart_add_view, name='cart-add'),
    path('remove/<str:product_id>', cart_remove_view, name='cart-remove'),
]
