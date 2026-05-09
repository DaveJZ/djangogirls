from django.conf import settings
from django.db import models
from django.utils import timezone

class FoodItem(models.Model):
    name = models.CharField(max_length=200)
    stock_level = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DONATE', 'Donate'),
        ('TAKE', 'Take'),
    ]
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='transactions')
    person_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name}"