from blog.models import Article
from product.models import Product
from shop.models import Shop


def latest_products_context_processor(request):
    products = Product.published.all()[:4]
    return {'latest_products': products}


def latest_articles_context_processor(request):
    articles = Article.published.all()[:4]
    return {'latest_articles': articles}


def latest_shops_context_processor(request):
    shops = Shop.active.all()[:4]
    return {'latest_shops': shops}