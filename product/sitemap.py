from django.contrib.sitemaps import Sitemap
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Product.objects.filter(product_type='multiple', is_active=True)

    def lastmod(self, obj):
        return obj.created
