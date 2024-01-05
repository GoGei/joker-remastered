import django_tables2 as tables
from core.User.models import User


class UsersTable(tables.Table):
    id = tables.TemplateColumn(template_name='Admin/Users/users_table_id_field.html', orderable=True)
    actions = tables.TemplateColumn(template_name='Admin/Users/users_table_actions_field.html', orderable=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'is_active')
        template_name = "django_tables2/bootstrap4.html"
