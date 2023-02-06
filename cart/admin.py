from django.contrib import admin

# Register your models here.
from cart.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'name', 'phone_number')
    search_fields = ('city', 'full_address', 'phone_number', 'zip_code')
    list_filter = ('created',)
