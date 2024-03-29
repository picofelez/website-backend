import json

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import formset_factory, modelformset_factory
from django.http import JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from cart.models import Transportation
from account.models import User
from core.forms import RatingForm
from core.models import Rating
from product.models import Product, PriceHistory
from shop.filters import ShopFilter
from shop.forms import ContactForm, WalletForm, ShopInvoiceForm, ShopInvoiceDetailForm
from shop.mixins import ShopPanelAccessMixin
from shop.models import Shop, SellerInformation, Wallet, ShopInvoice, ShopInvoiceDetail


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

    def get_context_data(self, *args, **kwargs):
        context = super(ShopAccountMainView, self).get_context_data(*args, **kwargs)
        context['weekly_records'] = ShopInvoice.objects.get_weekly_records(self.get_object())
        return context


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


@login_required
def create_shop_invoice_view(request, **kwargs):
    shop = get_object_or_404(Shop, owner=request.user, unique_uuid=kwargs.get('unique_uuid'))

    invoice_form = ShopInvoiceForm(request.POST or None)
    invoice_detail_formset = formset_factory(ShopInvoiceDetailForm, extra=0)
    formset = invoice_detail_formset(request.POST or None)

    if all([invoice_form.is_valid(), formset.is_valid()]):
        invoice = invoice_form.save(commit=False)
        username = request.POST.get('username')
        if username:
            user = User.objects.get(username=username)
            invoice.user = user
        invoice.shop = shop
        invoice.save()
        for form in formset:
            factor_detail = form.save(commit=False)
            factor_detail.invoice = invoice
            factor_detail.save()

        return redirect(
            reverse_lazy(
                'shop:shop-panel-invoices',
                kwargs={'unique_uuid': kwargs.get('unique_uuid')}
            )
        )

    context = {
        'shop': shop,
        'factor_form': invoice_form,
        'factor_detail_formset': formset,
        'form_length': 0
    }
    return render(request, 'shop/panel/shop_invoice_create_update.html', context)


@login_required
def update_shop_invoice_view(request, *args, **kwargs):
    shop = get_object_or_404(Shop, owner=request.user, unique_uuid=kwargs.get('unique_uuid'))

    invoice = get_object_or_404(ShopInvoice, pk=kwargs.get('pk'))
    invoice_form = ShopInvoiceForm(request.POST or None, instance=invoice)
    invoice_detail_formset = modelformset_factory(
        ShopInvoiceDetail, form=ShopInvoiceDetailForm, extra=0, can_delete=True
    )
    qs = invoice.invoice_details.all()
    formset = invoice_detail_formset(request.POST or None, queryset=qs)

    if all([invoice_form.is_valid(), formset.is_valid()]):
        invoice = invoice_form.save(commit=False)
        username = request.POST.get('username')
        if username:
            user = User.objects.get(username=username)
            invoice.user = user
        invoice.shop = shop
        invoice.save()

        for form in formset:
            factor_detail = form.save(commit=False)
            factor_detail.invoice = invoice
            if form.cleaned_data['DELETE']:
                factor_detail.delete()
            else:
                factor_detail.save()

        return redirect(
            reverse_lazy(
                'shop:shop-panel-invoices-detail',
                kwargs={'pk': invoice.pk, 'unique_uuid': kwargs.get('unique_uuid')}
            )
        )

    context = {
        'factor_form': invoice_form,
        'factor_detail_formset': formset,
        'factor': invoice,
        'form_length': qs.count(),
        'shop': shop
    }
    return render(request, 'shop/panel/shop_invoice_create_update.html', context)


def customer_for_invoice_ajax_view(request, **kwargs):
    """
    return customer detail.
    """
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == "POST":
            data = json.load(request)
            customer_data = data.get('payload')
            try:
                user = User.objects.get(username=customer_data.get('phone'))
                return JsonResponse({
                    'status': 'success',
                    'phone': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })
            except User.DoesNotExist:
                user = User(
                    username=customer_data.get('phone'),
                    last_name=customer_data.get('first_name'),
                    first_name=customer_data.get('last_name')
                )
                user.save()
                return JsonResponse({
                    'status': 'success',
                    'phone': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })
        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')
