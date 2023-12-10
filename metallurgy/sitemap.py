from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from .models import WorkSample


class WorkSampleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return WorkSample.objects.filter(status='p', publish_time__lte=timezone.now())

    def lastmod(self, obj):
        return obj.created
