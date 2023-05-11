from django import forms
from clients.models import Transfer
from .models import BankingHistory
from crispy_forms.bootstrap import PrependedText, Field, AppendedText
from crispy_forms.helper import FormHelper, Layout
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.utils.safestring import mark_safe

class DateInput(forms.DateInput):
    input_type = 'date'


class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': '7'}))


class TransferForm(forms.Form):
    beneficiary_bank_address = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    pin = forms.IntegerField()
    amount = forms.DecimalField()
    IBAN = forms.CharField(max_length=34, required=False)
    receivers_name = forms.CharField(max_length=30)
    beneficiary_account_number = forms.CharField(max_length=15)
    country = CountryField(blank_label="(Select country)").formfield(widget =  CountrySelectWidget())
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        self.fields["amount"].widget.attrs.update(  
            {'class': 'form-control-lg '})
        self.fields['amount'].label = 'Amount in <span class="text-primary fw-bolder h5">$</span>'
        
        self.fields["country"].widget.attrs.update(
            {'class': 'form-control-lg rounded-4'})
        self.fields["pin"].widget.attrs.update(
            {'class': 'form-control-lg rounded-4'})
        self.fields["IBAN"].widget.attrs.update(
            {'class': 'form-control-lg rounded-4'})
        self.fields["receivers_name"].widget.attrs.update(
            {'class': 'form-control-lg rounded-4'})
        self.fields["beneficiary_account_number"].widget.attrs.update(
            {'class': 'form-control-lg rounded-4'})
        
        # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Field(PrependedText('amount','<i class="bi bi-currency-dollar form-control-lg" style="font-size:14px; border-radius:inherit"></i>',  active=True,  css_class="form-control form-control-lg text-info"))
        # )
        

class LoadBalanceForm(forms.Form):
    amount = forms.DecimalField()
    

class AddHistoryForm(forms.ModelForm):
    transaction_date = forms.DateField(widget=DateInput)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'name':'body', 'rows':'3'}))
    class Meta:
        model = BankingHistory
        fields = ['record','amount', 'transaction_date', 'description']
    