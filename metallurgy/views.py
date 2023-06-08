from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from metallurgy.filters import WorkSampleFilter
from metallurgy.mixins import CustomerProjectAccessMixin, CustomerInvoiceAccessMixin
from metallurgy.models import WorkSample, Project, Invoice


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


class WorkSampleDetailView(DetailView):
    model = WorkSample
    template_name = 'metallurgy/work_sample_detail.html'


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
