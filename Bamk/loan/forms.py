# loan/forms.py
from django import forms

class LoanRequestForm(forms.Form):
    """Formulaire pour soumettre une demande de prêt"""
    State = forms.CharField(
        label="État",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    NAICS = forms.IntegerField(
        label="Code NAICS",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    NewExist = forms.ChoiceField(
        label="Type d'entreprise",
        choices=[(1, "Nouvelle entreprise"), (2, "Entreprise existante")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    RetainedJob = forms.IntegerField(
        label="Emplois conservés",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    FranchiseCode = forms.IntegerField(
        label="Code franchise",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    UrbanRural = forms.ChoiceField(
        label="Zone",
        choices=[(1, "Urbain"), (2, "Rural"), (0, "Non défini")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    GrAppv = forms.FloatField(
        label="Montant du prêt ($)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    Bank = forms.CharField(
        label="Banque",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    Term = forms.IntegerField(
        label="Durée (mois)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    class Meta:
        fields = ['State', 'NAICS', 'NewExist', 'RetainedJob', 'FranchiseCode', 'UrbanRural', 'GrAppv', 'Bank', 'Term']
    
    def save(self, commit=True):
        pass