from datetime import date as date_cls

from django import forms


def gbp_str_to_pence(value: str) -> int:
    value = (value or "").strip().replace("£", "")
    if value == "":
        return 0
    # basic safe parse to pennies
    pounds, dot, pennies = value.partition(".")
    pounds_i = int(pounds) if pounds else 0
    pennies = (pennies + "00")[:2]
    pennies_i = int(pennies)
    return pounds_i * 100 + pennies_i


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
        return gbp_str_to_pence(self.cleaned_data["amount_gbp"])


class IncomeForm(forms.Form):
    date = forms.DateField(input_formats=["%Y-%m-%d"])
    description = forms.CharField(max_length=255)
    amount_gbp = forms.CharField()

    def clean_amount_gbp(self):
        return gbp_str_to_pence(self.cleaned_data["amount_gbp"])


class ExpenseForm(IncomeForm):
    pass