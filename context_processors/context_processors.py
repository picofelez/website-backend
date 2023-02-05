from blog.models import Article
from product.models import Product


def latest_products_context_processor(request):
    products = Product.published.all()[:4]
    return {'latest_products': products}


def latest_articles_context_processor(request):
    articles = Article.published.all()[:4]
    return {'latest_articles': articles}
