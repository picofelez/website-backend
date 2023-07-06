from django import forms
from jalali_date.widgets import AdminJalaliDateWidget

from shop.models import Contact, ShopInvoice, ShopInvoiceDetail


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('full_name', 'subject', 'phone', 'message', 'shop')


class WalletForm(forms.Form):
    sheba = forms.CharField(
        widget=forms.TextInput
    )


class ShopInvoiceForm(forms.ModelForm):
    class Meta:
        model = ShopInvoice
        fields = '__all__'
        widgets = {
            'date': AdminJalaliDateWidget(
                attrs={'autocomplete': 'off', }
            ),
            'life_time': AdminJalaliDateWidget(
                attrs={'autocomplete': 'off', }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop'].required = False
        self.fields['user'].required = False


class ShopInvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = ShopInvoiceDetail
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control py-5 py-md-3', 'placeholder': 'نام'}
            ),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control py-5 py-md-3', 'placeholder': 'مقدار'}
            ),
            'quantity_name': forms.TextInput(
                attrs={'class': 'form-control py-5 py-md-3', 'placeholder': 'واحد'}
            ),
            'amount': forms.NumberInput(
                attrs={'class': 'form-control py-5 py-md-3', 'placeholder': 'قیمت'}
            ),
            'count_of_order': forms.TextInput(
                attrs={'class': 'form-control py-5 py-md-3', 'placeholder': 'تعداد'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice'].required = False
