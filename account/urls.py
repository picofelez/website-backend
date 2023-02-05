from django.urls import path
from .views import login_view, register_view, verify_otp_view, complete_register_view

app_name = 'account'
urlpatterns = [
    path('login/', login_view, name='otp-login'),
    path('register/', register_view, name='otp-register'),
    path('otp/verify', verify_otp_view, name='otp-verify'),
    path('register/complete', complete_register_view, name='complete-register'),
]
