from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render

from account.forms import PhoneNumberForm

# Create your views here.
from extensions.send_otp import send_otp

User = get_user_model()


def login_view(request):
    form = PhoneNumberForm(request.POST or None)

    if form.is_valid():
        phone_number = form.cleaned_data.get('phone_number')
        user_exist: bool = User.objects.filter(username=phone_number)

        if not user_exist:
            messages.error(request, 'شماره یافت نشد، لطفا روی گزینه ثبت نام کلیک کنید.')
        else:
            send_otp(request, phone_number)
            # TODO: redirect user to verify otp page.

    context = {
        'form': form
    }
    return render(request, 'account/phone_auth.html', context)
