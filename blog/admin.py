from django.contrib import admin
from .models import Tag, Article


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class TagArticleInline(admin.TabularInline):
    model = Article.tags.through
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'status')
    list_filter = ('created',)
    search_fields = ('title', 'summary', 'description')
    list_editable = ('status',)
    fieldsets = (
        ('اطلاعات مقاله', {'fields': ('title', 'summary', 'keywords', 'description')}),
        ('تصویر و نویسنده', {'fields': ('image',)}),
        ('وضعیت مشاهده', {'fields': ('publish_time', 'status')}),
    )

    inlines = [
        TagArticleInline
    ]
