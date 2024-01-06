import json

from django import forms
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.Utils.Filters.filtersets import BaseFilterForm
from core.Joke.models import Joke


class JokeFilterForm(BaseFilterForm):
    class Meta(BaseFilterForm.Meta):
        search_fields = ('text', 'slug')
        model = Joke


class JokeForm(forms.ModelForm):
    text = forms.CharField(label='Joke text', max_length=4096, required=True,
                           widget=CKEditorUploadingWidget(config_name='jokes',
                                                          attrs={'class': 'form-control'}))
    slug = forms.SlugField(required=True)

    class Meta:
        model = Joke
        fields = ('text', 'slug')

    def clean(self):
        data = super(JokeForm, self).clean()

        slug = data.get('slug')

        instance = self.instance
        qs = Joke.objects.filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            self.add_error('slug', _('With this slug joke already exists. Please, change a slug of joke!'))
        return data


class JokeAddForm(JokeForm):
    pass


class JokeEditForm(JokeForm):
    pass


class JokeImportForm(forms.Form):
    file = forms.FileField(label='Joke file', required=True,
                           widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.json'}))

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.json'):
            self.add_error('file', _('Only JSON files are allowed'))
        return file

    def run(self, data=None):
        try:
            if not data:
                data = self.cleaned_data.get('file').read().decode()
                data = json.loads(data)
        except UnicodeDecodeError:
            raise forms.ValidationError(_('Only JSON files are allowed'))
        except json.decoder.JSONDecodeError:
            raise forms.ValidationError(_('Invalid JSON file'))

        try:
            Joke.import_from_data(data)
        except Exception as e:
            raise forms.ValidationError(str(e))
