from django.contrib import admin
from .models import BudgetCategory, Goal, Transaction

admin.site.register(BudgetCategory)
admin.site.register(Goal)
admin.site.register(Transaction)
