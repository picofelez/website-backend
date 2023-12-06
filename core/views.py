from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from django.utils import timezone

from core.models import Question
from metallurgy.models import WorkSample
from shop.forms import ContactForm


# Create your views here.


class Home(TemplateView):
    """
    index view.
    """

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['portfolio'] = WorkSample.objects.filter(status='p', publish_time__lte=timezone.now())[:3]
        return data
    template_name = 'core/home.html'


class AboutUsView(TemplateView):
    """
    About us view.
    """
    template_name = 'core/about-us.html'


class CreateContactView(SuccessMessageMixin, CreateView):
    """
    Contact us view.
    """
    template_name = 'core/contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact-us')
    success_message = 'پیام شما با موفقیت ارسال شد. با شما تماس خواهیم گرفت!'


class QuestionListView(ListView):
    """
    Faq view.
    """
    queryset = Question.objects.filter(status='a')
    template_name = 'core/faq.html'


class IronCalculatorTemplateView(TemplateView):
    template_name = 'core/calculator.html'
