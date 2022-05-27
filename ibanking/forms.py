from django import forms
from clients.models import Transfer
from django_countries.fields import CountryField

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': '7'}))


class TransferForm(forms.Form):
    beneficiary_bank_address = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    pin = forms.IntegerField()
    amount = forms.DecimalField()
    IBAN = forms.CharField(max_length=34, required=False)
    receivers_name = forms.CharField(max_length=30)
    beneficiary_account_number = forms.CharField(max_length=15)
    country = CountryField(blank=True).formfield()


class LoadBalanceForm(forms.Form):
    amount = forms.DecimalField()
    