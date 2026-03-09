from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("landing/", views.landing, name="landing_explicit"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),  # <-- add this
]