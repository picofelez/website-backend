from blog.models import Article
from cart.cart import Cart
from product.models import Product
from shop.models import Shop


def latest_products_context_processor(request):
    products = Product.published.all().select_related(None)[:4]
    return {'latest_products': products}


def latest_multiple_products_context_processor(request):
    products = Product.objects.filter(is_active=True, product_type='multiple').select_related(None)[:4]
    return {'latest_multiple_products': products}


def latest_articles_context_processor(request):
    articles = Article.published.all().select_related(None)[:3]
    return {'latest_articles': articles}


def latest_shops_context_processor(request):
    shops = Shop.active.all().select_related(None)[:4]
    return {'latest_shops': shops}


def cart_list_context_processor(request):
    cart = Cart(request)
    return {'cart': Cart(request)}
