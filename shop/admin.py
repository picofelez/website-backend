from django.contrib import admin

from .models import (
    Shop,
    Contact,
    SellerInformation,
    Wallet,
    WalletTransaction,
    ShopInvoice,
    ShopInvoiceDetail,
    ShopScoreHistory
)


# Register your models here.

class SellerInformationInline(admin.StackedInline):
    model = SellerInformation
    extra = 0


class WalletTransactionInline(admin.TabularInline):
    model = WalletTransaction
    readonly_fields = ('created_jalali',)
    extra = 0


class ShopInvoiceDetailInline(admin.TabularInline):
    model = ShopInvoiceDetail
    extra = 0


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'is_special')
    search_fields = ('title', 'slug')
    list_editable = ('status',)
    list_filter = ('status', 'is_special', 'created')
    readonly_fields = ('created', 'updated', 'unique_uuid')

    inlines = [
        SellerInformationInline
    ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
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


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_jalali', 'get_balance', 'confirmed')
    search_fields = ('sheba',)
    list_filter = ('confirmed',)
    readonly_fields = ('id',)

    inlines = [
        WalletTransactionInline
    ]


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'transaction_type', 'transaction_status', 'get_value', 'created_jalali')
    list_filter = ('transaction_type', 'transaction_status')


@admin.register(ShopInvoice)
class ShopInvoiceAdmin(admin.ModelAdmin):
    list_display = ('shop', 'invoice_shop', 'date', 'user', 'get_total_details_display', 'get_total_price_display')
    list_filter = ('date', 'created', 'invoice_shop')
    search_fields = ('shop__title', 'user__first_name', 'user__last_name')
    readonly_fields = ('created',)
    inlines = [
        ShopInvoiceDetailInline
    ]


@admin.register(ShopInvoiceDetail)
class ShopInvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('name', '__str__', 'quantity', 'quantity_name', 'get_total_price_display')
    list_filter = ('created',)
    search_fields = ('invoice__shop__title',)


@admin.register(ShopScoreHistory)
class ShopScoreHistoryAdmin(admin.ModelAdmin):
    pass
