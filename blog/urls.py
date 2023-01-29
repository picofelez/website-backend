from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView
)

app_name = 'blog'
urlpatterns = [
    path('list/', ArticleListView.as_view(), name='blog-list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='blog-detail'),
]
