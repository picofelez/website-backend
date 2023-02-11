from django.contrib import admin

from product.models import Product, Category, FavoriteProduct


# Register your models here.
class CategoryInline(admin.TabularInline):
    model = Category.products.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'shop', 'get_price', 'quantity', 'is_active', 'is_confirmed'
    )
    list_editable = ('is_confirmed',)
    list_filter = ('is_active', 'is_confirmed', 'created')
    search_fields = ('title', 'description', 'categories', 'id')
    fieldsets = (
        ('عنوان', {'fields': ('id', 'title', 'description', 'image')}),
        ('مالک', {'fields': ('shop', 'maker')}),
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
