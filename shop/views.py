from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.views.generic import DetailView

from shop.forms import CreateContact
from shop.models import Shop


# Create your views here.


class ShopDetailView(DetailView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_detail.html'


def create_shop_contact(request, **kwargs):
    form = CreateContact(request.POST or None)
    shop = get_object_or_404(Shop, status='a', slug=kwargs.get('slug'))

    if form.is_valid():
        shop_contact = form.save(commit=False)
        shop_contact.shop = shop
        shop_contact.save()

        messages.success(request, 'پیام شما با موفقیت ارسال شد.')

    context = {
        'shop': shop,
        'form': form
    }
    return render(request, 'shop/shop_create_contact.html', context)
