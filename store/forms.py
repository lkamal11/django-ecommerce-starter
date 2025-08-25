
from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    address = forms.CharField(max_length=300)
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=20)
