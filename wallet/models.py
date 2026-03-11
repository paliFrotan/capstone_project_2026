from django.conf import settings
from django.db import models
from django.utils import timezone

def pence_to_gbp_str(pence: int) -> str:
    sign = "-" if pence < 0 else ""
    pence = abs(int(pence or 0))
    pounds = pence // 100
    pennies = pence % 100
    return f"{sign}£{pounds:,}.{pennies:02d}"

class StartingBalance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField(help_text="First day of the month (YYYY-MM-01)")
    amount_pence = models.IntegerField()

    class Meta:
        unique_together = ("user", "month")

    def __str__(self):
        return f"{self.user} {self.month:%Y-%m} {self.amount_pence}p"


class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    KIND_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=140)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    amount_pence = models.IntegerField(help_text="Positive integer pennies")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date", "-created_at"]
    def signed_amount_pence(self) -> int:
        p = int(self.amount_pence or 0)
        if str(self.kind).lower() == "expense":
            return -abs(p)
        return abs(p)

    @property
    def amount_str(self) -> str:
        # shows positive amount
        return pence_to_gbp_str(self.amount_pence)

    @property
    def signed_amount_str(self) -> str:
        # income = +£, expense = -£
        return pence_to_gbp_str(self.signed_amount_pence())    

    def signed_amount_pence(self) -> int:
        return self.amount_pence if self.kind == self.INCOME else -self.amount_pence

    def __str__(self):
        return f"{self.user} {self.date} {self.kind} {self.amount_pence}p"