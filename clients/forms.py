from django import forms
from django.contrib.auth.models import User
from .models import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from allauth.account.forms import SignupForm, LoginForm
from django_countries.fields import CountryField
from django.utils import timezone
from . import models
from django_countries import widgets, countries
from random import randrange



gender = (
        ('male', 'MALE'),
        ('female', 'FEMALE')
    )


class DateInput(forms.DateInput):
    input_type = 'date'


class SelfLoginForm (LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"] = forms.CharField(label='user ID')
        self.fields["login"].widget.attrs.update(
            {'class': 'form-control-lg rounded-pill border-0 shadow-sm mb-3'})
        self.fields["password"].widget.attrs.update(
            {'class': 'form-control-lg rounded-pill border-0 shadow-sm mb-3 '})


class MyCustomSignupForm(SignupForm):
    # field_order = ['first_name', 'last_name',  'username',
    #                'email', 'password1', 'password2', 'balance','country', 'address', 'dob','image']
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last name')
    balance = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':'3'}))
    country = CountryField(blank=True).formfield()
    dob = forms.DateField(widget=DateInput)
    gender = forms.ChoiceField(choices=gender)
    image = forms.ImageField(required=False)

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        number = [randrange(10) for i in range(10)]
        acc_number = ''.join(str(i) for i in number)
        pin = acc_number[:4]
        models.Client.objects.create(
                user=user, 
                balance=self.cleaned_data['balance'], 
                address=self.cleaned_data['address'], 
                country=self.cleaned_data['country'], 
                dob=self.cleaned_data['dob'],
                gender = self.cleaned_data['gender'],
                account_number = acc_number,
                transfer_pin = pin

        )
        return user

    def __init__(self, *args, **kwargs):

        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = ""
        self.fields["last_name"].widget.attrs["placeholder"] = ""
        self.fields["email"].widget.attrs["placeholder"] = ""
        self.fields["username"].widget.attrs["placeholder"] = ""
        self.fields["password1"].widget.attrs["placeholder"] = ""
        self.fields["password2"].widget.attrs["placeholder"] = ""

        self.fields["first_name"].widget.attrs.update({'class': 'form-control-lg'})
        self.fields["last_name"].widget.attrs.update({'class': 'form-control-lg'})
        self.fields["email"].widget.attrs.update({'class': 'form-control-lg'})
        self.fields["username"].widget.attrs.update({'class': 'form-control-lg'})
        self.fields["balance"].widget.attrs.update({'class': 'form-control-lg'})
        self.fields["country"].widget.attrs.update({'class': 'form-control-lg'})



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username']


class ClientUpdateForm(forms.ModelForm):
    country = CountryField(blank=True).formfield()
    class Meta:
        model = Client
        fields = ['image','country', 'gender', 'dob']


class DeactivateUser(forms.Form):
    deactivate = forms.BooleanField()

class UserForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField()
    username = UsernameField(
        label='User ID',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class ClientRegisterForm(forms.ModelForm):
    balance = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':'3'}))
    country = CountryField(blank=True).formfield()
    dob = forms.DateField(widget=DateInput)
    gender = forms.ChoiceField(choices=gender)
    image = forms.ImageField(required=False)
    class Meta:
        model = Client
        fields =  ['balance', 'address', 'country', 'dob', 'gender', 'image']

class TransferSuccessForm(forms.Form):
    is_success = forms.BooleanField()


class ChangePinForm(forms.Form):
    current_pin = forms.CharField(max_length=30)
    new_pin = forms.CharField(max_length=30)
    new_pin_again = forms.CharField(max_length=30)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=30)
    password_again = forms.CharField(max_length=30)