from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from blog.filters import ArticleFilter
from blog.models import Article

from core.forms import RatingForm

# Create your views here.
from core.models import Rating


class ArticleListView(FilterView):
    """
    This view show all published article.
    """
    queryset = Article.published.all()
    template_name = 'blog/blog_list.html'
    paginate_by = 12
    filterset_class = ArticleFilter


class ArticleDetailView(FormMixin, DetailView):
    queryset = Article.published.all()
    template_name = 'blog/blog_detail.html'
    form_class = RatingForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        form.fields['comment'].required = True

        if form.is_valid() and self.request.user.is_authenticated:
            rate = Rating(
                comment=form.cleaned_data.get('comment'),
                content_object=self.get_object(),
                user=self.request.user
            )
            rate.save()

            messages.success(request, 'نظر شما با موفقیت ارسال شد.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('blog:blog-detail', args=[self.get_object().id])
