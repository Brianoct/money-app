from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, BudgetCategory, Goal
from .forms import TransactionForm
from django.db.models import Sum
from datetime import datetime

@login_required
def record_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stats')
    else:
        form = TransactionForm()
    return render(request, 'moneyapp/record.html', {'form': form})

@login_required
def stats(request):
    total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    categories = BudgetCategory.objects.all()
    category_stats = []
    for cat in categories:
        spent = Transaction.objects.filter(
            type='expense', category=cat, date__month=datetime.today().month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        category_stats.append({'name': cat.name, 'spent': spent, 'budget': cat.budget_amount})
    goals = Goal.objects.all()
    goal_stats = []
    for goal in goals:
        allocated = Transaction.objects.filter(type='income', goal=goal).aggregate(Sum('amount'))['amount__sum'] or 0
        goal_stats.append({'name': goal.name, 'allocated': allocated, 'target': goal.target_amount})
    return render(request, 'moneyapp/stats.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'category_stats': category_stats,
        'goal_stats': goal_stats,
    })

@login_required
def settings(request):
    categories = BudgetCategory.objects.all()
    goals = Goal.objects.all()
    return render(request, 'moneyapp/settings.html', {'categories': categories, 'goals': goals})