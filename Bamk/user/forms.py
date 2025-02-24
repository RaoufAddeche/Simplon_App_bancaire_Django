from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    advisor = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=False,
        help_text="Select your banking advisor (optional)"
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
