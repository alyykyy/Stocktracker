from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Stock(models.Model):
    CATEGORY_CHOICES = [
        ('non_critical', 'Non-Critical'),
        ('critical', 'Critical'),
        ('expendable', 'Expendable'),
        ('diagnostics', 'Diagnostics'),
        ('consumable', 'Consumable'),
        ('implants', 'Implants'),
        ('equipment', 'Equipment'),
    ]

    stock_key = models.CharField(max_length=50, unique=True)
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField()
    supplier = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name
    
    def is_expired(self):
        return timezone.now().date() > self.expiry_date

    def is_almost_expired(self):
        today = timezone.now().date()
        return today < self.expiry_date <= today + timedelta(days=30)

    def is_critically_low(self):
        return self.quantity <= 10

    def is_low(self):
        return 10 < self.quantity <= 20

class Inventory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.item_name} - {self.quantity}"