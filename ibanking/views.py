from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib import messages
from .forms import ContactForm, TransferForm
from django.contrib.auth.decorators import login_required
from clients.models import Transfer, Client
from django.core.mail import send_mail

# Create your views here.

def index(request):
    return render(request, 'ibanking/index.html')

def charity(request):
    return render(request, 'ibanking/charity.html')

def contact(request):
    form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'ibanking/contact.html', context)


@login_required
def transfer(request, username):
    user =  get_object_or_404(Client, user = request.user)
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            amount = form.cleaned_data['amount']
            transfer_pin = request.user.profile.transfer_pin
            if not int(pin) == int(transfer_pin):
                messages.error(request, "wrong pin entered.")
            elif (user.balance - 150) <= amount:
                    messages.warning(request, "balance too low, Balance shouldnt be less than $150 after transfer.")
            else:
                obj, created = Transfer.objects.get_or_create(
                    user = request.user,
                    amount= amount,
                    IBAN= form.cleaned_data['IBAN'],
                    receivers_name= form.cleaned_data['receivers_name'],
                    beneficiary_account_number= form.cleaned_data['beneficiary_account_number'],
                    beneficiary_bank_address= form.cleaned_data['beneficiary_bank_address'],
                    country= form.cleaned_data['country']
                )
                
                print(user.balance)
                user.balance -= form.cleaned_data['amount']
                user.save()
                # EMAILING 
                subject = f"Transfer Processing."
                message = f"Account with the username: {user.user.username}, initiated a transfer.\nAmount: {form.cleaned_data['amount']} \nIgnore if this mail it wasn't you."
                sender = "mickeyjayblest@gmail.com"
                send_mail(
                    subject,
                    message,
                    'mickeyjayblest@gmail.com',
                    [user.user.email, 'ukejemichael@gmail.com']
                )
                messages.success(request,'Transfer Has Been Submitted \nTransfer Under Processing');
                return redirect("userprofile", request.user.username)

    else:
        form = TransferForm()
    context = {
        'form': form
    }
    return render(request, 'ibanking/make_transfer.html', context)
