# inventory/forms.py
from django import forms
from .models import Stock, Inventory

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['stock_key', 'item_name', 'category', 'quantity', 'expiry_date', 'supplier']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['quantity']

