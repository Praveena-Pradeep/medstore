from django import forms
from .models import Medicine, Stock

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'price']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantity']
