from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.http import Http404
from django.shortcuts import render, redirect

from account.forms import PhoneNumberForm, VerifyOtpForm
from extensions.utils import get_client_ip
from extensions.send_otp import send_otp

# Create your views here.

User = get_user_model()


def login_view(request):
    form = PhoneNumberForm(request.POST or None)

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
                    print('created')
                    # TODO: redirect user to complete information page.
                else:
                    login(request, user=user)
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
