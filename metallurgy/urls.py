from django.urls import path
from .views import metallurgy_landing_view, WorkSampleDetailView

app_name = 'metallurgy'
urlpatterns = [
    path('', metallurgy_landing_view, name='landing'),
    path('<int:pk>/<str:title>', WorkSampleDetailView.as_view(), name='work-sample-detail'),
]
