from import_export import resources, fields, widgets

from account.models import User
from metallurgy.models import Project


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
