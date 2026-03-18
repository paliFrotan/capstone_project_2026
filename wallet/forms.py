from datetime import date as date_cls
from .utils import parse_amount   # or wherever you placed it
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Optional.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

class StartingBalanceForm(forms.Form):
    month = forms.DateField(
        input_formats=["%Y-%m"],
        help_text="YYYY-MM",
        widget=forms.TextInput(attrs={"placeholder": "YYYY-MM"}),
    )
    amount_gbp = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "0.00"}))

    def clean_month(self):
        m = self.cleaned_data["month"]
        return date_cls(m.year, m.month, 1)

    def clean_amount_gbp(self):
        value = self.cleaned_data.get("amount_gbp")
        amount = parse_amount(value)
        if amount is None:
            raise forms.ValidationError("Amount must be a valid number.")
        return amount


class IncomeForm(forms.Form):
    date = forms.DateField(input_formats=["%Y-%m-%d"])
    description = forms.CharField(max_length=255)
    amount_gbp = forms.CharField()

    def clean_amount_gbp(self):
        value = self.cleaned_data.get("amount_gbp")
        amount = parse_amount(value)
        if amount is None:
            raise forms.ValidationError("Amount must be a valid number.")
        return amount


class ExpenseForm(IncomeForm):
    pass