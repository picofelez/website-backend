from django import forms

from shop.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('full_name', 'subject', 'phone', 'message', 'shop')


class WalletForm(forms.Form):
    sheba = forms.CharField(
        widget=forms.TextInput
    )
