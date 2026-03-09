from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

    
# Create your views here.

def landing(request):
    return render(request, "wallet/landing.html")

def dashboard(request):
    # For demonstration, we'll just redirect to the dashboard with some query parameters
    from datetime import date
    selected_month = date.today().replace(day=1)  # First day of the current month
    selected_date = date.today()  # Today's date
    url = reverse("dashboard") + f"?month={selected_month:%Y-%m}&date={selected_date:%Y-%m-%d}"
    return redirect(url)
    
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