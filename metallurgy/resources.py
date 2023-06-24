from import_export import resources, fields, widgets

from account.models import User
from metallurgy.models import Project, Invoice, InvoiceDetail


class ProjectResources(resources.ModelResource):
    customers = fields.Field(
        column_name='customers',
        attribute='customers',
        widget=widgets.ManyToManyWidget(User, field='username', separator=' , ')
    )

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'customers', 'start_date', 'end_date', 'accessibility_status', 'is_paid'
        )
        export_order = (
            'id', 'name', 'description', 'customers', 'start_date', 'end_date', 'accessibility_status', 'is_paid'
        )


class InvoiceResource(resources.ModelResource):
    project_name = fields.Field(
        column_name='project_name',
        attribute='project_name',
        widget=widgets.ForeignKeyWidget(Project, field='name')
    )

    class Meta:
        model = Invoice
        fields = (
            'id', 'date', 'project', 'description', 'is_paid', 'accessibility_status'
        )
        export_order = (
            'id', 'date', 'project', 'project_name', 'description', 'is_paid', 'accessibility_status'
        )


class InvoiceDetailResource(resources.ModelResource):
    class Meta:
        model = InvoiceDetail
        fields = (
            'id', 'invoice', 'name', 'quantity', 'quantity_name', 'amount'
        )
        export_order = (
            'id', 'invoice', 'name', 'quantity', 'quantity_name', 'amount'
        )
