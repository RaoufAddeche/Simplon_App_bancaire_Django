from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # On récupère l'utilisateur sans le passer à `super()`
        super(NewsForm, self).__init__(*args, **kwargs)
        self.user = user  # Stocke l'utilisateur pour une utilisation dans `clean()`

    def clean_created_by(self):
        user = self.cleaned_data["created_by"]
        if not user.is_staff:
            raise forms.ValidationError("Seuls les utilisateurs staff peuvent être auteurs d'articles.")
        return user