from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from wallet.views import (
    landing,
    month_transactions,
    transaction_edit,
    transaction_delete,
)

urlpatterns = [
    path("landing/", landing, name="landing"),
    path("", landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),


    # Auth (named routes match your template usage)
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    path("month/", month_transactions, name="month_transactions"),
    path("transaction/<int:pk>/edit/", transaction_edit, name="transaction_edit"),
    path("transaction/<int:pk>/delete/", transaction_delete, name="transaction_delete"),
]