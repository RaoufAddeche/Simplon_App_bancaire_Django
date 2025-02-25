from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a Username'})
        )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter an Email'})
        )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
    )
    advisor = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=True,
        widget=forms.Select(),
        empty_label="Select an advisor"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'advisor']

    def save(self, commit=True):
        user = super().save(commit=commit)
        advisor = self.cleaned_data.get('advisor')
        # Save the advisor information in the related Profile.
        profile = user.profile
        profile.advisor = advisor
        if commit:
            profile.save()
        return user
