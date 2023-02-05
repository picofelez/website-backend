from product.models import Product


def latest_products_context_processor(request):
    products = Product.published.all()[:4]
    return {'latest_products': products}
