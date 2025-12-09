from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    """Form for creating and updating Transaction instances."""
    class Meta:
        model = Transaction
        fields = ['date', 'name',
                  'amount', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'maxlength': 255}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'category': forms.Select(),
        }