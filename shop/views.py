from django.shortcuts import render

from django.views.generic import DetailView

from shop.models import Shop
# Create your views here.


class ShopDetailView(DetailView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_detail.html'
