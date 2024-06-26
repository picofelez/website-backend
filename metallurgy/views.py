import urllib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from metallurgy.filters import WorkSampleFilter
from metallurgy.mixins import CustomerProjectAccessMixin, CustomerInvoiceAccessMixin
from metallurgy.models import WorkSample, Project, Invoice
from product.models import Category


# Create your views here.


def metallurgy_landing_view(request):
    portfolio = WorkSample.objects.filter(status='p', publish_time__lte=timezone.now())[:3]

    context = {
        'portfolio': portfolio
    }
    return render(request, 'metallurgy/abdi_metal_landing.html', context)


class WorkSampleListView(FilterView):
    queryset = WorkSample.objects.filter(status='p', publish_time__lte=timezone.now())
    template_name = 'metallurgy/work_sample_list.html'
    paginate_by = 15
    filterset_class = WorkSampleFilter


class WorkSampleCategoryListView(ListView):
    model = WorkSample
    template_name = 'metallurgy/work_sample_list.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(WorkSampleCategoryListView, self).get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs.get("pk"))
        return context

    def get_queryset(self):
        return WorkSample.objects.filter(
            status='p', publish_time__lte=timezone.now(), categories=self.kwargs.get("pk")
        )


class CategoriesListView(ListView):
    queryset = Category.objects.filter(parent__isnull=True)
    template_name = 'metallurgy/work_sample_category_list.html'


class WorkSampleDetailView(DetailView):
    model = WorkSample
    template_name = 'metallurgy/work_sample_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(status='p', publish_time__lte=timezone.now())


class CustomerProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'metallurgy/customer_project_list.html'

    def get_queryset(self):
        return self.model.objects.filter(customers__in=[self.request.user])


class CustomerProjectDetailView(CustomerProjectAccessMixin, DetailView):
    model = Project
    template_name = 'metallurgy/customer_project_detail.html'


class CustomerInvoiceDetailView(CustomerInvoiceAccessMixin, DetailView):
    model = Invoice
    template_name = 'metallurgy/customer_invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerInvoiceDetailView, self).get_context_data(**kwargs)
        context['related_invoices'] = Invoice.objects.filter(
            project=self.get_object().project, accessibility_status='c'
        ).exclude(id=self.get_object().id)
        return context
