import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.views.generic import DetailView
from django_filters.views import FilterView

from shop.filters import ShopFilter
from shop.forms import ContactForm
from shop.models import Shop, SellerInformation


# Create your views here.


class ShopDetailView(DetailView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_detail.html'


class ShopProductsView(DetailView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_products.html'


def create_shop_contact(request, **kwargs):
    form = ContactForm(request.POST or None)
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


class ShopListView(FilterView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_list.html'
    paginate_by = 12
    filterset_class = ShopFilter


def register_shop(request):
    context = {}
    return render(request, 'shop/register_shop.html', context)


def register_shop_seller_information_create(request):
    """
    ajax view for save seller information.
    """
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == "POST":
            data = json.load(request)
            seller_data = data.get('payload')
            try:
                seller = SellerInformation(
                    phone_number=seller_data.get('phone_number'),
                    full_name=seller_data.get('full_name'),
                    national_code=seller_data.get('national_code'),
                    shop=request.user.shops.first()
                )
                seller.save()
                return JsonResponse({'status': 'success'})
            except:
                return JsonResponse({'status': 'fail'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')


def register_shop_create(request):
    """
    ajax view for save shop data.
    """
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            shop_data = data.get('payload')
            try:
                shop = Shop(
                    title=shop_data.get('shop_title'),
                    slug=shop_data.get('shop_slug'),
                    location=shop_data.get('shop_location'),
                    about=shop_data.get('shop_about'),
                    demand=shop_data.get('shop_demand'),
                    supply=shop_data.get('shop_supply'),
                    owner=request.user
                )
                shop.save()
                return JsonResponse({'status': 'success'})
            except:
                return JsonResponse({'status': 'fail'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')
