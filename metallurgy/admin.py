from django.contrib import admin
from .models import (
    WorkSample,
    WorkSampleImage,
    Project,
    Invoice,
    InvoiceDetail,
    ProjectTransaction
)
from import_export.admin import ExportActionMixin


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
class ProjectAdmin(ExportActionMixin, admin.ModelAdmin):
    list_filter = ('accessibility_status', 'created')
    list_display = ('name', 'get_total_expenses', 'get_total_expenses_paid', 'accessibility_status', 'is_paid')
    list_editable = ('accessibility_status',)
    search_fields = ('name', 'description', 'customers__last_name')
    filter_horizontal = ('customers', 'metal_orders')
    inlines = [
        InvoiceInline,
        MetalOrderInline,
        ProjectTransactionInline
    ]


@admin.register(Invoice)
class InvoiceAdmin(ExportActionMixin, admin.ModelAdmin):
    list_filter = ('date', 'is_paid', 'accessibility_status')
    list_display = ('__str__', 'get_humanized_invoice_price', 'is_paid')
    search_fields = ('description', 'project__name', 'project__customers__last_name')

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
