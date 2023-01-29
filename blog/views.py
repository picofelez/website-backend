from django.shortcuts import render

from django.views.generic import ListView
from blog.models import Article


# Create your views here.


class ArticleListView(ListView):
    queryset = Article.published.all()
    template_name = 'blog/blog_list.html'
    paginate_by = 12
