from django import forms
from django import forms
from .models import UnderContract

class UnderContractForm(forms.ModelForm):
    class Meta:
        model = UnderContract
        fields = ["address","category","flex_organic", "effective_date", "closing_date","price", "escrow","commission","mls_fee"]
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'closing_date': forms.DateInput(attrs={'type':'date'}),
            'price': forms.NumberInput(attrs={'placeholder': 'USD'}),
            'escrow': forms.NumberInput(attrs={'placeholder': 'USD'}),
            'commission': forms.NumberInput(attrs={'placeholder': "%"}),
            'mls_fee': forms.NumberInput(attrs={'placeholder': 'USD'})
        }
        
class UnderContractProcessing(forms.ModelForm):
    class Meta:
        model = UnderContract
        fields = ["notion","congratulations", "calendar", "flex_tracker", "loop"]
        
        
class UnderContractClosing(forms.ModelForm):
    class Meta:
        model = UnderContract
        fields = ["loop_closed","notion_closed","flex_closed","zillow_closed","kyn","close_pending"]