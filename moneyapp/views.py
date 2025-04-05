from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Transaction, BudgetCategory, Goal
from .forms import TransactionForm
from django.db.models import Sum
from datetime import datetime
import csv
from django.utils import translation
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def record_transaction(request):
    logger.info(f"Current language in record_transaction: {translation.get_language()}")
    transactions = Transaction.objects.all()
    filter_type = request.GET.get('filter_type', '')
    if filter_type:
        transactions = transactions.filter(type=filter_type)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Set the user to the logged-in user
            logger.info(f"Setting user for new transaction: {request.user.username}")
            transaction.save()
            logger.info(f"Transaction saved with user: {transaction.user.username if transaction.user else 'None'}")
            return redirect('stats')
    else:
        form = TransactionForm()
    return render(request, 'moneyapp/record.html', {
        'form': form,
        'transactions': transactions,
        'filter_type': filter_type,
    })

@login_required
def download_transactions_csv(request):
    logger.info(f"Current language in download_transactions_csv: {translation.get_language()}")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Type', 'Amount', 'Category', 'Goal', 'Description', 'User'])
    transactions = Transaction.objects.all()
    for transaction in transactions:
        user_name = transaction.user.username if hasattr(transaction, 'user') and transaction.user else 'N/A'
        writer.writerow([
            transaction.date,
            transaction.type,
            transaction.amount,
            transaction.category.name if transaction.category else 'N/A',
            transaction.goal.name if transaction.goal else 'N/A',
            transaction.description if transaction.description else 'N/A',
            user_name,
        ])
    return response

@login_required
def stats(request):
    logger.info(f"Current language in stats: {translation.get_language()}")
    total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    categories = BudgetCategory.objects.all()
    category_stats = []
    for cat in categories:
        spent = Transaction.objects.filter(
            type='expense', category=cat, date__month=datetime.today().month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        progress = (spent / cat.budget_amount * 100) if cat.budget_amount else 0
        category_stats.append({'name': cat.name, 'spent': spent, 'budget': cat.budget_amount, 'progress': progress})
    goals = Goal.objects.all()
    goal_stats = []
    for goal in goals:
        allocated = Transaction.objects.filter(type='income', goal=goal).aggregate(Sum('amount'))['amount__sum'] or 0
        progress = (allocated / goal.target_amount * 100) if goal.target_amount else 0
        goal_stats.append({'name': goal.name, 'allocated': allocated, 'target': goal.target_amount, 'progress': progress})
    return render(request, 'moneyapp/stats.html', {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'category_stats': category_stats,
        'goal_stats': goal_stats,
    })

@login_required
def settings(request):
    logger.info(f"Current language in settings: {translation.get_language()}")
    categories = BudgetCategory.objects.all()
    goals = Goal.objects.all()
    return render(request, 'moneyapp/settings.html', {'categories': categories, 'goals': goals})

def register(request):
    logger.info(f"Current language in register: {translation.get_language()}")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'moneyapp/register.html', {'form': form})

def set_language(request):
    lang = request.GET.get('lang', 'es')
    logger.info(f"Setting language to: {lang}")
    translation.activate(lang)
    request.session['django_language'] = lang
    logger.info(f"Active language after activation: {translation.get_language()}")
    translation_path = os.path.join(os.path.dirname(__file__), '..', 'locale', lang, 'LC_MESSAGES', 'django.mo')
    logger.info(f"Translation file path: {translation_path}, exists: {os.path.exists(translation_path)}")
    translated = translation.gettext("Money App")
    logger.info(f"Translated 'Money App' to: {translated}")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def check_superuser(request):
    logger.info(f"Current language in check_superuser: {translation.get_language()}")
    try:
        user = User.objects.get(username='brian', is_superuser=True)
        return HttpResponse(f"Superuser 'brian' exists with password hash: {user.password}")
    except User.DoesNotExist:
        return HttpResponse("Superuser 'brian' does not exist in the database.")