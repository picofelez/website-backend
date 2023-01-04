import os
import random


def generate_product_id():
    """
    generate random ID for product model.
    """
    number = random.randint(1000000, 9999999)
    return f"pcf-{number}"


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
