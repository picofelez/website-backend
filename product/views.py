from django.views.generic import DetailView, ListView
from .models import Product


# Create your views here.


class ProductDetailView(DetailView):
    """
    This view show a product detail.
    """
    queryset = Product.published.all()
    template_name = 'product/product_detail.html'
    context_object_name = 'product'


class ProductListView(ListView):
    """
    This view show all published products.
    """
    queryset = Product.published.all()
    template_name = 'product/product_list.html'
    paginate_by = 15
