from django.urls import path
from .views import metallurgy_landing_view, WorkSampleDetailView, CustomerProjectsListView

app_name = 'metallurgy'
urlpatterns = [
    path('', metallurgy_landing_view, name='landing'),
    path('portfolio/<int:pk>/<str:title>', WorkSampleDetailView.as_view(), name='work-sample-detail'),

    path('customer/projects/', CustomerProjectsListView.as_view(), name='customer-project-list'),
]
