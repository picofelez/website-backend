from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class Home(TemplateView):
    """
    index view.
    """
    template_name = 'core/home.html'