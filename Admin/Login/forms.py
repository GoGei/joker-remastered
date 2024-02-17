from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from core.User.models import User
from core.User.senders import AdminForgotPasswordSender


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', strip=True,
                               min_length=8, max_length=128,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    remember_me = forms.BooleanField(label='Remember Me', required=False)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError(_('This field is required.'))
        return password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        q = Q(email__iexact=email, is_active=True) & (Q(is_staff=True) | Q(is_superuser=True))
        user = User.objects.filter(q).first()
        if not user:
            raise forms.ValidationError(_('User with this email not found.'))
        else:
            self.cleaned_data['user'] = user

        return email

    def send_forgot_password(self):
        user = self.cleaned_data.get('user')
        AdminForgotPasswordSender().send(user)


class ForgotPasswordConfirmForm(forms.Form):
    password = forms.CharField(label='Password', strip=True,
                               min_length=8, max_length=128,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'password'}))
    repeat_password = forms.CharField(label='Repeat password', strip=True,
                                      min_length=8, max_length=128,
                                      widget=forms.PasswordInput(attrs={'autocomplete': 're-enter password'}))

    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')

        if not password:
            self.add_error('password', _('This field is required.'))
        if not repeat_password:
            self.add_error('repeat_password', _('This field is required.'))

        if password and repeat_password and password != repeat_password:
            self.add_error('password', _('Passwords do not match.'))
            self.add_error('repeat_password', _('Passwords do not match.'))

        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = self.user
        password = data.get('password')

        user.set_password(password)
        user.save()
        AdminForgotPasswordSender().delete(self.key)
        return user
