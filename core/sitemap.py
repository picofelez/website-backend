from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return [
            "core:home",
            "core:about-us",
            "core:contact-us",
            "metallurgy:landing",
            "core:calculator",
            "core:work-sample-list"
        ]

    def location(self, item):
        return reverse(item)
