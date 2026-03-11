from datetime import date as date_cls

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404

from .forms import ExpenseForm, IncomeForm, StartingBalanceForm
from .models import StartingBalance, Transaction

def landing(request):
    return render(request, "wallet/landing.html")


def pence_to_gbp_input_str(pence: int) -> str:
    """
    Format pence -> string suitable for your amount_gbp CharField, e.g. '12.34'.
    (No £ sign, because your gbp_str_to_pence strips it anyway.)
    """
    pence = int(pence or 0)
    sign = "-" if pence < 0 else ""
    pence = abs(pence)
    pounds = pence // 100
    pennies = pence % 100
    return f"{sign}{pounds}.{pennies:02d}"



def month_first_day(d: date_cls) -> date_cls:
    return date_cls(d.year, d.month, 1)


def next_month_first_day(d: date_cls) -> date_cls:
    if d.month == 12:
        return date_cls(d.year + 1, 1, 1)
    return date_cls(d.year, d.month + 1, 1)


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    today = date_cls.today()

    # --- Read selected date ---
    date_param = request.GET.get("date")
    if date_param:
        try:
            yyyy, mm, dd = date_param.split("-")
            selected_date = date_cls(int(yyyy), int(mm), int(dd))
        except Exception:
            selected_date = today
    else:
        selected_date = today

    # --- Month ALWAYS follows the selected date ---
    selected_month = month_first_day(selected_date)
    month_end = next_month_first_day(selected_month)

    # --- Forms ---
    starting_balance_form = StartingBalanceForm(
        initial={"month": f"{selected_month:%Y-%m}", "amount_gbp": "0.00"}
    )
    income_form = IncomeForm()
    expense_form = ExpenseForm()

    # --- POST actions ---
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "set_starting_balance":
            starting_balance_form = StartingBalanceForm(request.POST)
            if starting_balance_form.is_valid():
                month_obj = starting_balance_form.cleaned_data["month"]
                month = date_cls(month_obj.year, month_obj.month, 1)
                amount_pence = starting_balance_form.cleaned_data["amount_gbp"]

                StartingBalance.objects.update_or_create(
                    user=request.user,
                    month=month,
                    defaults={"amount_pence": amount_pence},
                )

                return redirect(
                    f"/dashboard/?month={month:%Y-%m}&date={selected_date:%Y-%m-%d}"
                )

        elif action == "add_income":
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                Transaction.objects.create(
                    user=request.user,
                    date=income_form.cleaned_data["date"],
                    description=income_form.cleaned_data["description"],
                    kind=Transaction.INCOME,
                    amount_pence=income_form.cleaned_data["amount_gbp"],
                )
                return redirect(
                    f"/dashboard/?month={selected_month:%Y-%m}&date={selected_date:%Y-%m-%d}"
                )

        elif action == "add_expense":
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                Transaction.objects.create(
                    user=request.user,
                    date=expense_form.cleaned_data["date"],
                    description=expense_form.cleaned_data["description"],
                    kind=Transaction.EXPENSE,
                    amount_pence=expense_form.cleaned_data["amount_gbp"],
                )
                return redirect(
                    f"/dashboard/?month={selected_month:%Y-%m}&date={selected_date:%Y-%m-%d}"
                )

    # --- Starting balance for the month ---
    starting_balance = StartingBalance.objects.filter(
        user=request.user, month=selected_month
    ).first()
    starting_pence = starting_balance.amount_pence if starting_balance else 0

    # --- Show ALL transactions for the month ---
    transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=selected_month,
        date__lt=month_end,
    ).order_by("date", "id")

    # --- Balance up to selected date ---
    signed_total = sum(
        t.signed_amount_pence() for t in transactions.filter(date__lte=selected_date)
    )
    balance_at_date_pence = starting_pence + signed_total

    context = {
        "selected_month": selected_month,
        "selected_date": selected_date,
        "starting_pence": starting_pence,
        "balance_at_date_pence": balance_at_date_pence,
        "transactions": transactions,
        "starting_balance_form": starting_balance_form,
        "income_form": income_form,
        "expense_form": expense_form,
        "starting_balance_str": pence_to_gbp_input_str(starting_pence),
        "balance_at_date_str": pence_to_gbp_input_str(balance_at_date_pence),
    }
    return render(request, "wallet/dashboard.html", context)




@login_required
def month_transactions(request):
    """
    Show all income + expenses for the selected month.
    If no month is provided, default to the current month.
    """

    # 1. Read month from URL: ?month=YYYY-MM
    month_param = request.GET.get("month")

    if month_param:
        yyyy, mm = month_param.split("-")
        month_start = date_cls(int(yyyy), int(mm), 1)
    else:
        today = date_cls.today()
        month_start = month_first_day(today)

    month_end = next_month_first_day(month_start)

    # 2. Query transactions for that month
    transactions = (
        Transaction.objects.filter(
            user=request.user,
            date__gte=month_start,
            date__lt=month_end,
        )
        .order_by("date", "id")
    )

    return render(
        request,
        "wallet/month_transactions.html",
        {
            "month_start": month_start,
            "transactions": transactions,
        },
    )
@login_required
def transaction_edit(request, pk: int):
    tx = get_object_or_404(Transaction, pk=pk, user=request.user)

    FormClass = IncomeForm if tx.kind == Transaction.INCOME else ExpenseForm

    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            tx.date = form.cleaned_data["date"]
            tx.description = form.cleaned_data["description"]
            tx.amount_pence = form.cleaned_data["amount_gbp"]
            tx.save()
            return redirect(f"/month-transactions/?month={tx.date:%Y-%m}")
    else:
        form = FormClass(
            initial={
                "date": tx.date,
                "description": tx.description,
                "amount_gbp": (tx.amount_pence or 0) / 100,
            }
        )

    return render(
        request,
        "wallet/transaction_edit.html",
        {"tx": tx, "form": form},
    )

@login_required
def transaction_delete(request, pk: int):
    """
    Confirm + delete.
    """
    tx = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == "POST":
        tx.delete()
        return redirect("month_transactions")

    return render(
        request,
        "wallet/transaction_delete.html",
        {"tx": tx},
    )