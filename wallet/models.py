from django.conf import settings
from django.db import models
from django.utils import timezone


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
        return self.amount_pence if self.kind == self.INCOME else -self.amount_pence

    def __str__(self):
        return f"{self.user} {self.date} {self.kind} {self.amount_pence}p"