from django import forms

from shop.models import Contact


class CreateContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('full_name', 'subject', 'phone', 'message', 'shop')
