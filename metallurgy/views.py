from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from metallurgy.mixins import CustomerProjectAccessMixin
from metallurgy.models import WorkSample, Project


# Create your views here.


def metallurgy_landing_view(request):
    portfolio = WorkSample.objects.filter(status='p', publish_time__lte=timezone.now())

    context = {
        'portfolio': portfolio
    }
    return render(request, 'metallurgy/abdi_metal_landing.html', context)


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
