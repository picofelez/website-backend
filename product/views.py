from django.views.generic import DetailView
from .models import Product


# Create your views here.


class ProductDetailView(DetailView):
    queryset = Product.published.all()
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
