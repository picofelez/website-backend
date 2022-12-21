from django.contrib import admin

from .models import Shop, Contact


# Register your models here.


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_thumbnail', 'owner', 'status', 'is_special')
    search_fields = ('title', 'owner', 'slug')
    list_editable = ('status',)
    list_filter = ('status', 'is_special', 'created')
    readonly_fields = ('created', 'updated')


@admin.register(Contact)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'phone', 'status')
    search_fields = ('full_name', 'phone')
    list_editable = ('status',)
    list_filter = ('status', 'created')
    readonly_fields = ('created', 'updated')