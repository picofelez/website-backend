from django.contrib import admin

from .models import Shop


# Register your models here.


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_thumbnail', 'owner', 'status', 'is_special')
    search_fields = ('title', 'owner', 'slug')
    list_editable = ('status',)
    list_filter = ('status', 'is_special', 'created')
    readonly_fields = ('created', 'updated')
