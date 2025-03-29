from django.contrib import admin
from django.urls import path
from moneyapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('record/', views.record_transaction, name='record_transaction'),
    path('stats/', views.stats, name='stats'),
    path('settings/', views.settings, name='settings'),
    path('', views.stats, name='home'),
]