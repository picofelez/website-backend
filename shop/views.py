import json

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from cart.models import Transportation
from core.forms import RatingForm
from core.models import Rating
from product.models import Product, PriceHistory
from shop.filters import ShopFilter
from shop.forms import ContactForm, WalletForm
from shop.mixins import ShopPanelAccessMixin
from shop.models import Shop, SellerInformation, Wallet, ShopInvoice


# Create your views here.


class ShopDetailView(DetailView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_detail.html'


class ShopProductsView(DetailView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_products.html'


class ShopRatingView(FormMixin, DetailView):
    queryset = Shop.active.all()
    template_name = 'shop/shop_rating.html'
    form_class = RatingForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        form.fields['rating'].required = True

        if form.is_valid() and self.request.user.is_authenticated:
            rate = Rating(
                stars=form.cleaned_data.get('rating'),
                content_object=self.get_object(),
                user=self.request.user
            )
            rate.save()

            messages.success(request, 'نظر شما با موفقیت ارسال شد.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('shop:shop-rating', args=[self.get_object().slug])


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


"""
From this line onwards, the views are related to the shop's panel.
"""


class ShopAccountMainView(ShopPanelAccessMixin, DetailView):
    model = Shop
    template_name = 'shop/panel/shop_main.html'

    def get_object(self, queryset=None):
        shop = get_object_or_404(Shop, unique_uuid=self.kwargs.get('unique_uuid'))
        return shop


class ShopUpdateView(ShopPanelAccessMixin, UpdateView):
    model = Shop
    template_name = 'shop/panel/shop_update.html'
    fields = ('title', 'image', 'about', 'demand', 'supply',)

    def get_success_url(self):
        return reverse_lazy('shop:shop-panel-main', args=[self.shop.unique_uuid])

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.shop.id, unique_uuid=self.shop.unique_uuid)


class ShopProductsListView(ShopPanelAccessMixin, ListView):
    model = Product
    template_name = 'shop/panel/shop_product_list.html'
    paginate_by = 15

    def get_queryset(self):
        return self.model.objects.filter(shop=self.shop)


class ShopProductUpdateView(ShopPanelAccessMixin, SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'shop/panel/shop_product_create_update.html'
    fields = (
        'title', 'description', 'stock', 'purchase_limit',
        'quantity', 'width', 'length', 'weight', 'image', 'is_active', 'categories'
    )
    success_message = 'تغییرات با موفقیت اعمال شد'

    def get_success_url(self):
        return reverse_lazy(
            'shop:shop-panel-products',
            kwargs={'unique_uuid': self.shop.unique_uuid}
        )


class ShopProductCreateView(ShopPanelAccessMixin, SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'shop/panel/shop_product_create_update.html'
    fields = (
        'title', 'description', 'stock', 'purchase_limit',
        'quantity', 'width', 'length', 'weight', 'image', 'is_active', 'categories', 'price'
    )
    success_message = 'محصول با موفقیت ایجاد شد'

    def get_success_url(self):
        return reverse_lazy(
            'shop:shop-panel-products',
            kwargs={'unique_uuid': self.shop.unique_uuid}
        )

    def form_valid(self, form):
        product = form.save(commit=False)
        product.maker = self.request.user
        product.shop = self.shop
        return super(ShopProductCreateView, self).form_valid(form)


class ShopOrderListView(ShopPanelAccessMixin, ListView):
    model = Transportation
    template_name = 'shop/panel/shop_order_list.html'
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.filter(shop=self.shop)


class ShopOrderDetailView(ShopPanelAccessMixin, DetailView):
    model = Transportation
    template_name = 'shop/panel/shop_order_detail.html'


class ShopOrderUpdateView(ShopPanelAccessMixin, UpdateView):
    model = Transportation
    template_name = 'shop/panel/shop_order_update.html'
    fields = ('expense',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().status != 'pending':
            raise Http404
        return super(ShopOrderUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('shop:shop-panel-orders-detail', args=[
            self.shop.unique_uuid, self.get_object().pk
        ])

    def form_valid(self, form):
        # TODO: send notification to buyer.
        transport = form.save(commit=False)
        transport.status = 'confirmed'
        transport.save()
        return super(ShopOrderUpdateView, self).form_valid(form)


@login_required
def shop_wallet_view(request, unique_uuid):
    context = {}
    shop = get_object_or_404(Shop, unique_uuid=unique_uuid, owner=request.user)
    wallet, created = Wallet.objects.get_or_create(user=request.user, shop=shop)

    if not wallet.sheba and not wallet.confirmed:
        wallet_form = WalletForm(request.POST or None)
        context['form'] = wallet_form

        if wallet_form.is_valid():
            wallet.sheba = wallet_form.cleaned_data.get('sheba')
            wallet.save()

    context['shop'] = shop
    context['wallet'] = wallet

    return render(request, 'shop/panel/shop_wallet.html', context)


class ShopUpdateProductPriceView(ShopPanelAccessMixin, UpdateView):
    model = Product
    template_name = 'shop/panel/shop_update_product_price.html'
    fields = ('price',)

    def get_success_url(self):
        return reverse_lazy('shop:shop-panel-products-update-price', args=[
            self.shop.unique_uuid,
            self.get_object().id
        ])

    def form_valid(self, form):
        product_form = form.save(commit=False)
        price_history = PriceHistory(product=self.get_object(), price=product_form.price, is_confirmed=True)

        product_form.save()
        price_history.save()
        return super(ShopUpdateProductPriceView, self).form_valid(form)


class ShopInvoiceListListView(ShopPanelAccessMixin, ListView):
    model = ShopInvoice
    template_name = 'shop/panel/shop_invoice_list.html'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(shop=self.shop).select_related("user", "shop")


class ShopInvoiceDetailDetailView(ShopPanelAccessMixin, DetailView):
    model = ShopInvoice
    template_name = 'shop/panel/shop_invoice_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(shop=self.shop)
