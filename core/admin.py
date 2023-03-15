from django.contrib import admin
from .models import Question, Rating


# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_filter = ('content_type',)
