from django.db import models
from django.utils import timezone
from clients.models import User
from decimal import Decimal

# Create your models here.

class BankingHistory(models.Model):
    RECORD = (
        ('credit', 'CREDIT'),
        ('debit', 'DEBIT')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history")
    record = models.CharField(default='credit', choices=RECORD, max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    amt_aft_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description =models.TextField(null=True, blank=True)
    transaction_date = models.DateField(default=timezone.now)

    
    def save(self, *args, **kwargs):
        if self.record == 'credit':
            self.amt_aft_charges = self.amount - (self.amount * Decimal(0.02))    
            self.balance += self.amt_aft_charges  
        else:
            self.amt_aft_charges  = self.amount + (self.amount *Decimal( 0.02))
            self.balance -= self.amt_aft_charges  
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_date}"