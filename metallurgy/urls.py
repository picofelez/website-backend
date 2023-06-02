from django.urls import path
from .views import (
    metallurgy_landing_view,
    WorkSampleDetailView,
    CustomerProjectsListView,
    CustomerProjectDetailView,
    CustomerInvoiceDetailView
)

app_name = 'metallurgy'
urlpatterns = [
    path('', metallurgy_landing_view, name='landing'),
    path('portfolio/<int:pk>/<str:title>', WorkSampleDetailView.as_view(), name='work-sample-detail'),

    path('customer/projects/', CustomerProjectsListView.as_view(), name='customer-project-list'),
    path('customer/projects/<int:pk>', CustomerProjectDetailView.as_view(), name='customer-project-detail'),

    path('customer/invoices/<int:pk>', CustomerInvoiceDetailView.as_view(), name='customer-invoice-detail'),
]
