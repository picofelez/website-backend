import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from account.forms import PhoneNumberForm, VerifyOtpForm, RegisterForm
from cart.models import Address, Order
from extensions.utils import get_client_ip
from extensions.send_otp import send_otp

# Create your views here.
from product.models import FavoriteProduct
from shop.models import ShopInvoice

User = get_user_model()


def login_view(request):
    form = PhoneNumberForm(request.POST or None)
    ip = get_client_ip(request)
    next_url = request.GET.get('next')

    if next_url:
        cache.set(f"{ip}-for-next-url", next_url, 500)

    if form.is_valid():
        phone_number = form.cleaned_data.get('phone_number')
        user_exist: bool = User.objects.filter(username=phone_number).exists()

        if not user_exist:
            messages.error(request, 'شماره یافت نشد، لطفا روی گزینه ثبت نام کلیک کنید.')
        else:
            send_otp(request, phone_number)
            return redirect('account:otp-verify')

    context = {
        'form': form
    }
    return render(request, 'account/phone_auth.html', context)


def register_view(request):
    form = PhoneNumberForm(request.POST or None)

    if form.is_valid():
        phone_number = form.cleaned_data.get('phone_number')
        user_exist: bool = User.objects.filter(username=phone_number).exists()

        if user_exist:
            messages.error(request, 'حسابی با این شماره موبایل قبلا ایجاد شده است.')
        else:
            send_otp(request, phone_number)
            return redirect('account:otp-verify')

    context = {
        'form': form
    }
    return render(request, 'account/phone_auth.html', context)


def verify_otp_view(request):
    form = VerifyOtpForm(request.POST or None)

    ip = get_client_ip(request)
    phone = cache.get(f"{ip}-for-authentication")
    otp = cache.get(phone)
    next_url = cache.get(f"{ip}-for-next-url")

    if phone is None:
        raise Http404

    if form.is_valid():
        received_code = form.cleaned_data.get('code')

        if otp is not None:
            if otp == received_code:
                user, created = User.objects.get_or_create(username=phone)
                cache.delete(phone)
                cache.delete(f"{ip}-for-authentication")

                if created:
                    login(request, user=user)
                    return redirect('account:complete-register')
                else:
                    login(request, user=user)
                    if next_url:
                        return redirect(next_url)
                    return redirect('core:home')
            else:
                messages.error(request, 'کد تائید اشتباه وارد شده است.')
        else:
            messages.error(request, 'کد تائید منقضی شده.')

    context = {
        'form': form,
        'phone': phone
    }
    return render(request, 'account/verify_otp.html', context)


def complete_register_view(request):
    form = RegisterForm(request.POST or None)
    ip = get_client_ip(request)
    next_url = cache.get(f"{ip}-for-next-url")

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        raise Http404

    if form.is_valid():
        cd = form.cleaned_data  # cleaned data

        user.first_name = cd.get('first_name')
        user.last_name = cd.get('last_name')
        user.set_password(cd.get('password'))
        user.save()

        login(request, user)
        if next_url:
            return redirect(next_url)
        return redirect('core:home')

    context = {
        'form': form
    }
    return render(request, 'account/complete_register.html', context)


@login_required
def user_profile_view(request):
    context = {}
    return render(request, 'account/user_profile.html', context)


class UserFavoriteProductView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    template_name = 'account/user_favorite_list.html'
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


def user_add_delete_favorite_product_view(request):
    """
    ajax view for add or delete user favorite product.
    """
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax and request.user.is_authenticated:
        if request.method == "POST":
            data = json.load(request)
            pd = data.get('payload')  # product data

            favorite_product, created = FavoriteProduct.objects.get_or_create(
                user=request.user, product_id=pd.get('product_id')
            )

            if created:
                return JsonResponse({'status': 'success'})
            else:
                favorite_product.delete()
                return JsonResponse({'status': 'deleted'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')


class UserAddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'account/user_address_list.html'
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserAddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Address
    template_name = 'account/user_address_create_update.html'
    fields = '__all__'
    success_message = 'created'

    def form_valid(self, form):
        address_form = form.save(commit=False)
        address_form.user = self.request.user
        address_form.save()
        return super(UserAddressCreateView, self).form_valid(form)

    def get_success_url(self):
        redirect_url = self.request.GET.get('redirect')
        if redirect_url and redirect_url == '/cart/checkout':
            return reverse('cart:cart-checkout')
        return reverse('account:user-address-list')


class UserAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Address
    template_name = 'account/user_address_create_update.html'
    success_url = reverse_lazy('account:user-address-list')
    fields = '__all__'
    success_message = 'updated'

    def form_valid(self, form):
        address_form = form.save(commit=False)
        address_form.user = self.request.user
        address_form.save()
        return super(UserAddressUpdateView, self).form_valid(form)


def user_delete_address_view(request, address_pk):
    """
    ajax view for delete user address.
    """
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    if is_ajax and request.user.is_authenticated:
        address = get_object_or_404(Address, id=address_pk, user=request.user)

        if request.method == "DELETE":
            address.delete()
            return JsonResponse({'status': 'deleted'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'account/user_order_list.html'
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'account/user_order_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account/user_profile_update.html'
    fields = ('first_name', 'last_name', 'email')
    success_url = reverse_lazy('account:user-profile')

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)


class UserShopInvoiceDetailView(LoginRequiredMixin, DetailView):
    model = ShopInvoice
    template_name = 'account/user_shop_invoice_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserShopInvoiceDetailView, self).get_context_data(**kwargs)
        context['related_invoices'] = ShopInvoice.objects.filter(
            user=self.request.user
        ).exclude(id=self.get_object().id)
        return context
