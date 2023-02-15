import json

from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView

from cart.cart import Cart
from cart.forms import CheckoutForm
from cart.models import Address, Order, OrderDetail, Transportation
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


def checkout_view(request):
    form = CheckoutForm(request.POST or None)

    if form.is_valid():
        cd = form.cleaned_data  # cleaned data

        # get address
        address = get_object_or_404(Address, id=cd.get('address'), user=request.user)
        # get or create order
        order, created = Order.objects.get_or_create(user=request.user, is_paid=False, address__isnull=True)

        # save order's address
        order.address = address
        order.save()

        # create order detail items from cart object
        cart = Cart(request)
        order_details = []
        for product in cart:
            order_details.append(
                OrderDetail(
                    order=order,
                    product=product.get('product'),
                    count=product.get('count'),
                    price=product.get('price')
                )
            )
        OrderDetail.objects.bulk_create(order_details)

        # create transportations
        shops = []
        transportation = []
        for order_detail in order_details:
            shop_id = order_detail.product.shop.id
            if shop_id not in shops:
                shops.append(shop_id)
                transportation.append(
                    Transportation(
                        shop=order_detail.product.shop, order=order
                    )
                )
        Transportation.objects.bulk_create(transportation)

        # clear cart
        cart.clear()

        messages.success(request, message='سفارش با موفقیت ثبت شد.')
        return redirect('account:user-order-detail', pk=order.id)

    context = {
        'form': form
    }
    return render(request, 'cart/checkout.html', context)


class CartListView(TemplateView):
    template_name = 'cart/cart_list.html'
