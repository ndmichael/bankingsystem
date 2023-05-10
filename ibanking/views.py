from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import BankingHistory
from clients.models import Client
from .forms import ContactForm, TransferForm, LoadBalanceForm, AddHistoryForm
from django.contrib.auth.decorators import login_required
from clients.models import Transfer, Client
from django.core.mail import send_mail
from decimal import Decimal

# Create your views here.

def index(request):
    return render(request, 'ibanking/index.html', {'title': 'home'})

def charity(request):
    return render(request, 'ibanking/charity.html', {'title': 'charity'})

def invest(request):
    return render(request, 'ibanking/investing.html', {'title': 'investment'})

def banking_history(request, username):
    user = User.objects.get(username=username)
    client = Client.objects.get(user=user)
    if request.method == "POST":
        form = AddHistoryForm(request.POST)   
        if form.is_valid():
            record = form.cleaned_data['record']
            set_form = form.save(commit=False)
            set_form.user = user
            set_form.balance = client.balance            
            set_form.save() 
            current_balance = BankingHistory.objects.all().order_by("-transaction_date").first()
            client.balance = current_balance.balance                           
            client.save()

            messages.success(request, f"banking history added.")
            return redirect(
                "banking_history", user.username
            ) 
    form = AddHistoryForm()
    context = {
        'user': user,
        'title': 'add history',
        'form': form,
    }
    print(user)
    return render(request, 'ibanking/manage_history.html', context)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # send_mail(
            #     subject,
            #     message,
            #     email,
            #     ['MICKEY@boiworldwide.com']
            # )
            messages.success(request,'Mail successfully sent.');
            redirect('contact')

    form = ContactForm()
    context = {
        'form': form,
        'title': 'contact us'
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
                
                # print(user.balance)
                # user.balance -= form.cleaned_data['amount']
                # user.save()
                # EMAILING 
                # subject = f"Transfer Processing."
                # message = f"Account with the username: {user.user.username}, initiated a transfer.\nAmount: {form.cleaned_data['amount']} \nIgnore if this mail it wasn't you."
                # sender = "mickeyjayblest@gmail.com"
                # send_mail(
                #     subject,
                #     message,
                #     'mickeyjayblest@gmail.com',
                #     [user.user.email, 'ukejemichael@gmail.com']
                # )
                messages.success(request,'Transfer Has Been Submitted. Transfer is Under Processing.');
                return redirect("userprofile", request.user.username)

    else:
        form = TransferForm()
    context = {
        'form': form,
        'title': 'transfer-page'
    }
    return render(request, 'ibanking/make_transfer.html', context)

def loadbalance(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("userprofile", request.user.username)
    
    if request.POST:
        id = request.POST.get('id')
        client = get_object_or_404(Client, user = id)
        print(client)
        if  request.POST:
            amount = int(request.POST.get('amount'))
            client.balance += amount
            client.save()
            messages.success(
                request, f"{client.user.username} current balance is {client.balance}."
            )
        return redirect(
                "loadbalance"
            )  
    else:
        loadbalanceform = LoadBalanceForm()
    clients = Client.objects.all().filter(user__is_active=True).order_by('-created')
    context = {
        'loadbalanceform' : loadbalanceform,
        'clients': clients,
        'title': 'load balance'
    }
    return render(request, 'ibanking/load_balance.html', context)
