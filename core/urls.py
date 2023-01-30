from django.urls import path

from .views import (
    Home,
    AboutUsView,
    CreateContactView
)

app_name = 'core'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', CreateContactView.as_view(), name='contact-us'),
]
