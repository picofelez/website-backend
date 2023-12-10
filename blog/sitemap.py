from django.contrib.sitemaps import Sitemap
from .models import Article


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Article.published.all()

    def lastmod(self, obj):
        return obj.created
