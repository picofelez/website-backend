import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cart.cart import Cart
from product.models import Product


# Create your views here.


def cart_add_view(request, product_id):
    """
    Add new product to cart.
    """
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            cd = data.get('payload')  # cleaned data
            count = cd.get('count')

            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id, is_confirmed=True, is_active=True)

            if int(count) <= product.purchase_limit and int(count) <= product.stock:
                cart.add(product, count=int(count), override_count=True)
                return JsonResponse({'status': 'added'})
            return JsonResponse({'status': 'failed'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')


def cart_remove_view(request, product_id):
    """
        Remove new product to cart.
    """
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'DELETE':
            cart = Cart(request)
            product = get_object_or_404(Product, id=product_id, is_confirmed=True, is_active=True)

            cart.remove(product)
            return JsonResponse({'status': 'deleted', 'total_price': cart.get_total_price()})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')


class CartListView(TemplateView):
    template_name = 'cart/cart_list.html'
