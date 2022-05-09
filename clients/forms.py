from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm, LoginForm
from django_countries.fields import CountryField
from django.utils import timezone
from . import models
from django_countries import widgets, countries
from random import randrange



class DateInput(forms.DateInput):
    input_type = 'date'


class SelfLoginForm (LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].widget.attrs.update(
            {'class': 'form-control-lg rounded-pill border-0 shadow-sm'})
        self.fields["password"].widget.attrs.update(
            {'class': 'form-control-lg rounded-pill border-0 shadow-sm  '})


class MyCustomSignupForm(SignupForm):
    field_order = ['first_name', 'last_name',
                   'email', 'username', 'password1', 'password2', 'balance','country', 'address', 'dob','image']
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last name')
    balance = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':'3'}))
    country = CountryField(blank=True).formfield()
    dob = forms.DateField(widget=DateInput)
    image = forms.ImageField(required=False)

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        number = [randrange(10) for i in range(10)]
        acc_number = ''.join(str(i) for i in number)
        pin = acc_number[:4]
        models.Client.objects.create(user=user, balance=self.cleaned_data['balance'], 
                address=self.cleaned_data['address'], 
                country=self.cleaned_data['country'], 
                dob=self.cleaned_data['dob'],
                account_number = acc_number,
                transfer_pin = pin

        )
        return user

    def __init__(self, *args, **kwargs):

        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "first name"
        self.fields["last_name"].widget.attrs["placeholder"] = "last name"

# class MyCustomSignupForm(SignupForm):
#         field_order = ['first_name', 'last_name', 'password1', 'password2', 'username', 'email',]
#         def __init__(self, *args, **kwargs):
#             super(MyCustomSignupForm, self).__init__(*args, **kwargs)
#             self.fields['first_name'] = forms.CharField(required=True)
#             self.fields['last_name'] = forms.CharField(required=True)
#             self.fields["email"].label = ''
#             self.fields["username"].label = ''
#             self.fields["password1"].label = ''
#             self.fields["password2"].label = ''
#             default_field_order = ['first_name', 'last_name', 'password1', 'password2', 'username', 'email',]

#         def save(self, request):
#             field_order = ['first_name', 'last_name', 'password1', 'password2', 'username', 'email',]
#             first_name = self.cleaned_data['first_name']
#             user = super(MyCustomSignupForm, self).save(request)
#             return user
