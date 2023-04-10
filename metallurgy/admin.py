from django.contrib import admin
from .models import WorkSample, WorkSampleImage


# Register your models here.
class WorkSampleImageInline(admin.TabularInline):
    model = WorkSampleImage
    extra = 0


@admin.register(WorkSample)
class WorkSampleAdmin(admin.ModelAdmin):
    inlines = [
        WorkSampleImageInline
    ]


@admin.register(WorkSampleImage)
class WorkSampleImage(admin.ModelAdmin):
    pass
