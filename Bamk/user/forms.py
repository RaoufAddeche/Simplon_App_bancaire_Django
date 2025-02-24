from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    username = forms.CharField(
        label="Username",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    last_name = forms.CharField(
        label="Last name",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    first_name = forms.CharField(
        label="First name",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    email = forms.EmailField(
        label="Email address",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("last_name", "first_name", "email", "password1", "password2")
