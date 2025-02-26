from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "description", "content", "image"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # On récupère l'utilisateur sans le passer à `super()`
        super(NewsForm, self).__init__(*args, **kwargs)
        # Stocke l'utilisateur pour une utilisation dans `clean()`

    def clean(self):
        cleaned_data = super().clean()

        if not self.user:  # ✅ Vérification si l'utilisateur est bien passé
            raise forms.ValidationError("L'utilisateur doit être connecté.")

        if not self.user.is_staff:  # ✅ Vérification du rôle
            raise forms.ValidationError("Seuls les utilisateurs staff peuvent créer des articles.")

        return cleaned_data