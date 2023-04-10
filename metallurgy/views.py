from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView

from metallurgy.models import WorkSample


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
