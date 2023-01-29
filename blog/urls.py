from django.urls import path
from .views import (
    ArticleListView
)

app_name = 'blog'
urlpatterns = [
    path('list/', ArticleListView.as_view(), name='blog-list'),
]
