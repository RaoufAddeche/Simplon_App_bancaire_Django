from django import forms
from .models import LoanRequest

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['state', 'naics', 'new_exist', 'retained_job', 'franchise_code', 
                  'urban_rural', 'gr_appv', 'bank', 'term']
