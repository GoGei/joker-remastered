import django_tables2 as tables


class LoggerTable(tables.Table):
    class Meta:
        fields = ('key', 'level', 'stamp', 'description')
        template_name = "django_tables2/bootstrap4.html"


class LoggerObjectTable(tables.Table):
    class Meta:
        fields = ('key', 'level', 'stamp', 'description', 'obj_type', 'obj_id', 'user_id', 'data')
        template_name = "django_tables2/bootstrap4.html"
