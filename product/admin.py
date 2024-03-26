from django.contrib import admin

from product.models import Product, Category, FavoriteProduct, PriceHistory


# Register your models here.
class CategoryInline(admin.TabularInline):
    model = Category.products.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'get_price', 'quantity', 'is_active', 'is_confirmed'
    )
    list_editable = ('is_confirmed',)
    list_filter = ('product_type', 'is_active', 'is_confirmed', 'created')
    search_fields = ('title', 'description', 'categories', 'id')
    filter_horizontal = ('shops',)
    fieldsets = (
        ('عنوان', {'fields': ('id', 'title', 'description', 'summary', 'image', 'image_url')}),
        ('مالک', {'fields': ('shop', 'maker', 'product_type', 'shops')}),
        ('قیمت گذاری', {'fields': ('price', 'quantity', 'stock', 'purchase_limit')}),
        ('اطلاعات', {'fields': ('weight', 'length', 'width', 'keywords')}),
        ('وضعیت نمایش', {'fields': ('is_active', 'is_confirmed')}),
        ('تاریخ ها', {'fields': ('created', 'updated')}),
    )
    readonly_fields = ('id', 'created', 'updated')

    inlines = [
        CategoryInline
    ]


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    pass
