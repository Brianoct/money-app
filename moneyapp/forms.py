from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'type', 'category', 'goal', 'description']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        goal = cleaned_data.get('goal')
        if type == 'income' and not goal:
            self.add_error('goal', 'Goal is required for income.')
        elif type == 'expense' and not category:
            self.add_error('category', 'Category is required for expense.')
        return cleaned_data