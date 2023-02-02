from django.urls import path
from .views import login_view, register_view

app_name = 'account'
urlpatterns = [
    path('login/', login_view, name='otp-login'),
    path('register/', register_view, name='otp-register'),
]
