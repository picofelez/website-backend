from django.urls import path
from .views import (
    metallurgy_landing_view,
    CustomerProjectsListView,
    CustomerProjectDetailView,
    CustomerInvoiceDetailView,
)

app_name = 'metallurgy'
urlpatterns = [
    path('', metallurgy_landing_view, name='landing'),

    path('customer/projects/', CustomerProjectsListView.as_view(), name='customer-project-list'),
    path('customer/projects/<int:pk>', CustomerProjectDetailView.as_view(), name='customer-project-detail'),

    path('customer/invoices/<int:pk>', CustomerInvoiceDetailView.as_view(), name='customer-invoice-detail'),
]
