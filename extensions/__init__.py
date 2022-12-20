import os
import random


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_shop_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    number_random = random.randint(2000, 10000)
    final_name = f"{instance.slug}-{number_random}{ext}"
    return f"shop/thumbnail/{final_name}"
