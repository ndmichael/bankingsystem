from django.db import models
from django.utils import timezone
from clients.models import User

# Create your models here.

class BankingHistory(models.Model):
    RECORD = (
        ('credit', 'CREDIT'),
        ('debit', 'DEBIT')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history")
    record = models.CharField(default='credit', choices=RECORD, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default="0.0")
    description =models.TextField()
    transaction_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_date}"