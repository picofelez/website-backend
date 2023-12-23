from django.urls import path

from metallurgy.views import WorkSampleListView, WorkSampleDetailView, WorkSampleCategoryListView
from .views import (
    Home,
    AboutUsView,
    CreateContactView,
    QuestionListView,
    IronCalculatorTemplateView
)

app_name = 'core'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', CreateContactView.as_view(), name='contact-us'),
    # path('faq/', QuestionListView.as_view(), name='faq'),
    path('calculator/', IronCalculatorTemplateView.as_view(), name='calculator'),
    path('portfolios/', WorkSampleListView.as_view(), name='work-sample-list'),
    path('portfolios/<slug>', WorkSampleCategoryListView.as_view(), name='work-sample-category-list'),
    path('portfolios/<int:pk>/<str:title>', WorkSampleDetailView.as_view(), name='work-sample-detail'),
]
