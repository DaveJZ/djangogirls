from django.contrib import admin
from .models import FoodItem, Transaction

admin.site.register(FoodItem)
admin.site.register(Transaction)