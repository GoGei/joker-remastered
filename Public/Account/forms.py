from django import forms
from django.utils.translation import gettext_lazy as _
from core.User.models import User
from core.User.senders import PublicForgotPasswordSender, PublicRegistrationEmailSender


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', strip=True,
                               min_length=1, max_length=128,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    remember_me = forms.BooleanField(label='Remember Me', required=False)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError(_('This field is required.'))
        return password


class UserPasswordForm(forms.Form):
    password = forms.CharField(label='Password', strip=True,
                               min_length=8, max_length=128,
                               widget=forms.PasswordInput(attrs={'autocomplete': 'password'}))
    repeat_password = forms.CharField(label='Repeat password', strip=True,
                                      min_length=8, max_length=128,
                                      widget=forms.PasswordInput(attrs={'autocomplete': 're-enter password'}))

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


class RegisterForm(UserPasswordForm):
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users_qs = User.objects.filter(email__iexact=email)

        active = users_qs.filter(is_active=True).first()
        inactive = users_qs.filter(is_active=False).first()

        if active:
            self.add_error('email', _('User with this email already exists.'))
        elif inactive:
            msg = _('User with this email already waiting for confirmation. We will send message one more time')
            self.add_error('email', msg)
            PublicRegistrationEmailSender().send(inactive)

        return email

    def save(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.create_user(email=email, password=password, is_active=False)
        PublicRegistrationEmailSender().send(user)
        return user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if not user:
            raise forms.ValidationError(_('User with this email not found.'))
        else:
            self.cleaned_data['user'] = user

        return email

    def send_forgot_password(self):
        user = self.cleaned_data.get('user')
        PublicForgotPasswordSender().send(user)


class ForgotPasswordConfirmForm(UserPasswordForm):
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        user = PublicForgotPasswordSender().get(self.key)
        if not user:
            self.add_error(None, _('Key is invalid or expired!'))
        else:
            cleaned_data['user'] = user

        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = data.get('user')
        password = data.get('password')

        user.set_password(password)
        user.save()
        return user
