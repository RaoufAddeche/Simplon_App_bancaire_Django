from django import forms 

class LoanRequestForm(forms.Form):
    "Formulaire pour soumettre une demande de prêt"
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Montant du prêt")