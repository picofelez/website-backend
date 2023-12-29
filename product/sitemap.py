from django.contrib.sitemaps import Sitemap
from .models import Product, Category


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Product.objects.filter(product_type='multiple', is_active=True)

    def lastmod(self, obj):
        return obj.created


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Category.objects.filter(parent__isnull=False)
