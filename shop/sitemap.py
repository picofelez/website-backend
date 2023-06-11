from django.contrib.sitemaps import Sitemap
from .models import Shop


class ShopSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Shop.active.all()

    def lastmod(self, obj):
        return obj.created
