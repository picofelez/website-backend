from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from core.models import Question
from shop.forms import ContactForm


# Create your views here.


class Home(TemplateView):
    """
    index view.
    """
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
    success_message = 'پیام شما با موفقیت ارسال شد.'


class QuestionListView(ListView):
    """
    Faq view.
    """
    queryset = Question.objects.filter(status='a')
    template_name = 'core/faq.html'
