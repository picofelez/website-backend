from django import forms

from cart.models import Address


class CheckoutForm(forms.Form):
    address = forms.CharField(
        widget=forms.TextInput
    )
    description = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
