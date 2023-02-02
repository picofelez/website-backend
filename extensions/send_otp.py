import random

from django.core.cache import cache
from django.conf import settings

from extensions.utils import get_client_ip


def send_otp(request, phone):
    otp_code = random.randint(1000, 9999)
    ip = get_client_ip(request)
    cache.set(f"{ip}-for-authentication", phone, settings.EXPIRY_TIME_OTP)
    cache.set(phone, str(otp_code), settings.EXPIRY_TIME_OTP)

    # TODO: send otp code with SMS service.
    print(otp_code)
