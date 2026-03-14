from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView



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
    # Password reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # Auth (named routes match your template usage)
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    path("month/", month_transactions, name="month_transactions"),
    path("transaction/<int:pk>/edit/", transaction_edit, name="transaction_edit"),
    path("transaction/<int:pk>/delete/", transaction_delete, name="transaction_delete"),
    path('report/<int:year>/<int:month>/', views.print_month_report, name='print_month_report'),
    path('import-csv/', views.import_csv, name='import_csv'),

]
