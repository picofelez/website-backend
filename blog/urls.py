from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView
)

app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='blog-list'),
    path('<int:pk>/<title>', ArticleDetailView.as_view(), name='blog-detail'),
]
