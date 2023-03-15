from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django_filters.views import FilterView

from blog.filters import ArticleFilter
from blog.models import Article


# Create your views here.

class ArticleListView(FilterView):
    """
    This view show all published article.
    """
    queryset = Article.published.all()
    template_name = 'blog/blog_list.html'
    paginate_by = 12
    filterset_class = ArticleFilter


class ArticleDetailView(DetailView):
    queryset = Article.published.all()
    template_name = 'blog/blog_detail.html'
