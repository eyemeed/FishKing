#app/forms.py
from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class OrderForm(forms.Form):
    qty = forms.IntegerField(min_value=1)
    customer_name = forms.CharField()
    customer_phone = forms.CharField()
    customer_address = forms.CharField()