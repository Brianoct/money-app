from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'type', 'category', 'goal', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }