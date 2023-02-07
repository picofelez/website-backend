from django.contrib import admin
from cart.models import (
    Address,
    Order,
    OrderDetail,
    Transportation
)


# Register your models here.


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'name', 'phone_number')
    search_fields = ('city', 'full_address', 'phone_number', 'zip_code')
    list_filter = ('created',)


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail


class TransportationInline(admin.TabularInline):
    model = Transportation


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'total_order_detail_price', 'total_transportation_expense', 'amount_payable', 'is_paid'
    )
    list_filter = ('created', 'is_paid')
    search_fields = ('user',)

    inlines = [
        OrderDetailInline,
        TransportationInline
    ]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(Transportation)
class TransportationAdmin(admin.ModelAdmin):
    pass
