from django.urls import path

from shop.views import ShopDetailView
from .views import (
    Home
)

app_name = 'core'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<slug>', ShopDetailView.as_view(), name='shop-detail'),
]
