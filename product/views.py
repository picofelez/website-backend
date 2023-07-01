from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from core.forms import RatingForm
from core.models import Rating
from .filters import ProductFilter
from .models import Product


# Create your views here.


class ProductDetailView(FormMixin, DetailView):
    """
    This view show a product detail.
    """
    queryset = Product.published.all()
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    form_class = RatingForm
    success_message = 'نظر شما با موفقیت ارسال شد.'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        form.fields['comment'].required = True
        form.fields['rating'].required = True

        if form.is_valid() and self.request.user.is_authenticated:
            rate = Rating(
                comment=form.cleaned_data.get('comment'),
                stars=form.cleaned_data.get('rating'),
                content_object=self.get_object(),
                user=self.request.user
            )
            rate.save()

            messages.success(request, 'نظر شما با موفقیت ارسال شد.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['price_data'] = [price.price for price in self.get_object().price_histories.all()]
        context['price_labels'] = [price.created_jalali() for price in self.get_object().price_histories.all()]
        return context

    def get_success_url(self):
        return reverse_lazy('product:product-detail', args=[self.get_object().id])


class ProductListView(FilterView):
    """
    This view show all published products.
    """
    queryset = Product.objects.filter(product_type='multiple', is_active=True)
    template_name = 'product/product_list.html'
    paginate_by = 15
    filterset_class = ProductFilter


class MultipleProductDetailView(DetailView):
    queryset = Product.objects.filter(is_active=True)
    template_name = 'product/multiple_product_detail.html'
