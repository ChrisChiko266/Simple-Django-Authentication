from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

# Get user model currently in use
User = get_user_model()


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, required=True, label='Password',
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput, required=False, label='Remember me'
    )

    class Meta:
        model = User
        fields = ('email',)
        required = ('email',)
        labels = {
            'email': _('Email Address'),
        }


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(
        label='Confirmation Password', widget=forms.PasswordInput, required=True,
        help_text='Passwords are case-sensitive.',
    )

    class Meta:
        model = User
        fields = ('email', 'username',)
        required = ('email', 'username',)
        labels = {
            'email': _('Email Address'),
        }
        help_texts = {
            'email': _('An email will be sent to the address for verification.'),
            'username': _('Username may contain letters, numbers and symbols.'),
        }
