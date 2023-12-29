"""picofelez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.sitemap import ArticleSitemap
from core.sitemap import StaticViewSitemap
from metallurgy.sitemap import WorkSampleSitemap
from product.sitemap import ProductSitemap, CategorySitemap

sitemaps = {
    "statics": StaticViewSitemap,
    "products": ProductSitemap,
    "portfolio": WorkSampleSitemap,
    "articles": ArticleSitemap,
    "categories": CategorySitemap
}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap"
    ),

    path('', include('core.urls')),
    path('products/', include('product.urls')),
    path('blog/', include('blog.urls')),
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls')),
    path('metallurgy/', include('metallurgy.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
