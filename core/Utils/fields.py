from django import forms

from core.Utils.validators import (
    PhoneValidator, PasswordValidators
)


class PhoneField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(PhoneValidator)


class PasswordField(forms.CharField):
    def __init__(self, widget_attrs=None, *args, **kwargs):
        kwargs.setdefault('widget', forms.PasswordInput(attrs=widget_attrs or self.get_default_attrs()))
        super(PasswordField, self).__init__(*args, **kwargs)
        self.validators.append(PasswordValidators)

    @classmethod
    def get_default_attrs(cls):
        return {"data-toggle": "password"}
