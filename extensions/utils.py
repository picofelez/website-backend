import os
import random

from django.utils import timezone
from . import jalali


def generate_product_id() -> str:
    """
    generate random ID for product model.
    """
    number = random.randint(1000000, 9999999)
    return f"pcf-{number}"


def generate_order_id() -> int:
    """
    generate random ID for Order model.
    """
    number = random.randint(1000000, 9999999)
    return number


def get_filename_ext(filepath):
    """
    get file path & ext.
    """
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_shop_image_path(instance, filename):
    """
    set shops image path & name.
    """
    name, ext = get_filename_ext(filename)
    number_random = random.randint(2000, 10000)
    final_name = f"{instance.slug}-{number_random}{ext}"
    return f"shop/thumbnail/{final_name}"


def upload_product_image_path(instance, filename):
    """
    set products image path & name.
    """
    name, ext = get_filename_ext(filename)
    number_random = random.randint(2000, 1000000)
    final_name = f"{number_random}{ext}"
    return f"products/thumbnail/{final_name}"


def upload_article_image_path(instance, filename):
    """
    set articles image path & name.
    """
    name, ext = get_filename_ext(filename)
    number_random = random.randint(2000, 1000000)
    final_name = f"{number_random}-{timezone.now()}{ext}"
    return f"articles/thumbnail/{final_name}"


def slug_generator(slug) -> str:
    return slug.replace(' ', '-')


def jalali_converter_dict(time) -> dict:
    jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد',
               'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time_to_str = f'{time.year},{time.month},{time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]} '

    return {'day': time_to_list[2], 'month': time_to_list[1], 'year': time_to_list[0]}


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
