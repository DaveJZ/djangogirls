from django import forms
from django.contrib import admin
from .models import FoodItem, Transaction

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock_level')
    search_fields = ('name',)

class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        t_type = cleaned_data.get('transaction_type')

        # Logic check: Ensure taking an item doesn't exceed current stock
        if item and quantity and t_type == 'TAKE':
            if item.stock_level < quantity:
                raise forms.ValidationError(
                    f"Insufficient Stock! You are trying to take {quantity} units of {item.name}, but only {item.stock_level} are available."
                )
        return cleaned_data

class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display = ('item', 'transaction_type', 'quantity', 'person_name', 'date')
    list_filter = ('transaction_type', 'date')

admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Transaction, TransactionAdmin)