from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from moneyapp import views
from moneyapp.models import Transaction, BudgetCategory, Goal  # Corrected import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='moneyapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('record/', views.record_transaction, name='record_transaction'),
    path('download-csv/', views.download_transactions_csv, name='download_transactions_csv'),
    path('stats/', views.stats, name='stats'),
    path('settings/', views.settings, name='settings'),
    path('set-language/', views.set_language, name='set_language'),
    path('check-superuser/', views.check_superuser, name='check_superuser'),
    path('', views.stats, name='home'),
]