from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from core.User.models import User


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
        # user.send_forgot_password_email()
