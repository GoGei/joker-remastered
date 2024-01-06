import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from core.Joke.models import Joke


class JokesTable(tables.Table):
    text_start = tables.TemplateColumn(template_name='Admin/Joke/joke_table_text_start_field.html', orderable=False)
    slug = tables.TemplateColumn(template_name='Admin/Joke/joke_table_slug_start_field.html', orderable=False)
    is_active = tables.BooleanColumn(orderable=False)
    actions = tables.TemplateColumn(template_name='Admin/Joke/joke_table_actions_field.html', orderable=False)

    class Meta:
        model = Joke
        fields = ('pk', 'text_start', 'slug', 'is_active', 'actions')
        template_name = "django_tables2/bootstrap4.html"


class JokesTopTable(tables.Table):
    text_start = tables.TemplateColumn(template_name='Admin/Joke/joke_table_text_start_field.html', orderable=False)
    likes = tables.Column(orderable=False, verbose_name=_('Likes'), accessor='likes_annotated')

    class Meta:
        model = Joke
        fields = ('pk', 'text_start', 'likes')
        template_name = "django_tables2/bootstrap4.html"
