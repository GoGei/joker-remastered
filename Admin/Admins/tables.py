import django_tables2 as tables
from core.User.models import User


class AdminTable(tables.Table):
    id = tables.TemplateColumn(template_name='Admin/Admins/admins_table_id_field.html', orderable=True)
    actions = tables.TemplateColumn(template_name='Admin/Admins/admins_table_actions_field.html', orderable=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'is_active', 'is_staff', 'is_superuser')
        template_name = "django_tables2/bootstrap4.html"
