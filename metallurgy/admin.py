from django.contrib import admin
from .models import (
    WorkSample,
    WorkSampleImage,
    Project,
    Invoice,
    InvoiceDetail,
    ProjectTransaction
)


# Register your models here.
class WorkSampleImageInline(admin.TabularInline):
    model = WorkSampleImage
    extra = 0


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    show_change_link = True


class ProjectTransactionInline(admin.TabularInline):
    model = ProjectTransaction
    extra = 0
    show_change_link = True


class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 0


class MetalOrderInline(admin.TabularInline):
    model = Project.metal_orders.through
    extra = 0


@admin.register(WorkSample)
class WorkSampleAdmin(admin.ModelAdmin):
    inlines = [
        WorkSampleImageInline
    ]


@admin.register(WorkSampleImage)
class WorkSampleImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('accessibility_status', 'created')
    list_display = ('name', 'get_total_expenses', 'get_total_expenses_paid', 'accessibility_status', 'is_paid')
    list_editable = ('accessibility_status',)
    search_fields = ('name', 'description',)
    filter_horizontal = ('customers', 'metal_orders')
    inlines = [
        InvoiceInline,
        MetalOrderInline,
        ProjectTransactionInline
    ]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceDetailInline,
        ProjectTransactionInline
    ]


@admin.register(InvoiceDetail)
class InvoiceDetailAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectTransaction)
class ProjectTransactionAdmin(admin.ModelAdmin):
    pass
