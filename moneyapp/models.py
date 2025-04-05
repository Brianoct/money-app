from django.db import models
from django.contrib.auth.models import User

class BudgetCategory(models.Model):
    name = models.CharField(max_length=50)
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Goal(models.Model):
    name = models.CharField(max_length=50)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('income', 'Income'), ('expense', 'Expense')])
    category = models.ForeignKey(BudgetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # This field was added

    def __str__(self):
        return f"{self.type} - {self.amount} on {self.date}"