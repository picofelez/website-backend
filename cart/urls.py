from django.urls import path
from .views import (
    cart_add_view,
)

app_name = 'cart'
urlpatterns = [
    path('add/<str:product_id>', cart_add_view, name='cart-add'),
]
