from django.contrib import admin

from .models import Shop, Contact, SellerInformation


# Register your models here.

class SellerInformationInline(admin.StackedInline):
    model = SellerInformation


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'is_special')
    search_fields = ('title', 'owner', 'slug')
    list_editable = ('status',)
    list_filter = ('status', 'is_special', 'created')
    readonly_fields = ('created', 'updated', 'unique_uuid')

    inlines = [
        SellerInformationInline
    ]


@admin.register(Contact)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'phone', 'status')
    search_fields = ('full_name', 'phone')
    list_editable = ('status',)
    list_filter = ('status', 'created')
    readonly_fields = ('created', 'updated')


@admin.register(SellerInformation)
class SellerInformationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'shop')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('created',)
    readonly_fields = ('created', 'updated')
