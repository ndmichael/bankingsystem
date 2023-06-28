from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Client
from ibanking.models import BankingHistory
from django.contrib import messages
from .forms import (
    ClientUpdateForm, 
    UserUpdateForm, 
    DeactivateUser, 
    ClientRegisterForm, 
    UserForm, 
    TransferSuccessForm,
    ChangePinForm,
    ChangePasswordForm
)
from clients.models import Client, Transfer
from random import randrange
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password


from django.contrib.auth.views import LoginView
from django.urls import reverse

from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
        


# Create your views here.


@login_required
def profile(request, username):
    user = get_object_or_404(
        User, username=username
    )  # getting the current user passed to it
    profile = Client.objects.filter(user=user)
    transfers = Transfer.objects.filter(user=user, is_success=True)
    histories = BankingHistory.objects.filter(user=user).order_by('-transaction_date')[:10]
    total_transfers =  Transfer.objects.filter(user=user).count()
    print(total_transfers)
    context = {
        "user": user,
        "profile": profile,
        'total_transfers': total_transfers,
        'histories': histories,
        'title': 'profile',
        'transfers': transfers
    }
    return render(request, 'account/profile.html', context)


@login_required
def admin(request):
    if not request.user.is_staff:
        # return reverse('userprofile', kwargs={'username': request.user.username})
        return redirect("userprofile", username=request.user.username)
        
    clients = Client.objects.all().filter(user__is_active=True).order_by('-created')
    total_clients =  Client.objects.all().filter(user__is_active=True).count()
    pending_transfers =  Transfer.objects.all().filter(is_success=False).filter(user__is_active=True).count()
    context ={
        'clients': clients,
        'total_clients': total_clients,
        'pending_transfers': pending_transfers,
        'title': 'admin',
    }
    return render(request, 'users/admin.html', context)


@login_required
def register(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    if request.method == "POST":
        u_form = UserForm(request.POST)
        c_form = ClientRegisterForm(request.POST,  request.FILES)
        if u_form.is_valid() and c_form.is_valid():
            user = u_form.save()
            client = c_form.save(commit=False)
            number = [randrange(10) for i in range(10)]
            acc_number = ''.join(str(i) for i in number)
            pin = acc_number[:4]
            client.user = user
            client.transfer_pin = pin
            client.account_number = acc_number
            client.save()
            username = u_form.cleaned_data.get("username")

            # EMAILING 
            '''subject = f"Account Creation"
            message = f"""'success', Account has been created for {username}.
                password:....
            """
            sender = "mickeyjayblest@gmail.com"
            send_mail(
                subject,
                message,
                'mickeyjayblest@gmail.com',
                ['ukejemicheal@gmail.com']
            )'''

            messages.success(
                request, f"Account has been created for {username} you  can now login."
            )
            return redirect("all_users")
    else:
        u_form = UserForm()
        c_form = ClientRegisterForm()
    context = {
        'c_form': c_form,
        'u_form': u_form,
        'title': "Registeration"
    }
    return render(request, 'users/register.html', context)

@login_required
def all_users(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    if request.POST:
        username = request.POST.get('id')
        # user = User.objects.get(username=username)
        user = get_object_or_404(User, username=username)
        if  request.POST.get('deactivate') == 'on':
            user.is_active = False
            user.save()
            messages.success(
                request, f"{username} has been deactivated."
            )
        return redirect(
                "all_users"
            )  
    else:
        deactivate_form = DeactivateUser()
    
    clients = Client.objects.all().filter(user__is_active=True).order_by('-created')
    total_clients =  Client.objects.all().filter(user__is_active=True).count()
    context = {
        'clients': clients,
        'd_form': deactivate_form,
        'total_clients': total_clients,
        'title': 'users'
    }
    return render(request, 'users/all_users.html', context)

@login_required
def all_transfers(request):
    
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("userprofile", request.user.username)

    if request.method == 'POST' and request.POST.get('is_success') :

        transfer_id = request.POST.get('id')
        user = request.POST.get('user')
    

        transfer = get_object_or_404(Transfer, id=transfer_id)
        user =  get_object_or_404(Client, user=user)
        Bhistory = BankingHistory(user=user.user, record='debit', amount=transfer.amount, balance=user.balance, description='Transfer')
        # user.balance -= transfer.amount
        user.save()
        Bhistory.save()
        
        transfer.is_success = True
        transfer.save()
        # EMAILING 
        # subject = f"Transfer Confirmation."
        # message = f"'success', Account has been created for {transfer.user.username}."
        # sender = "mickeyjayblest@gmail.com"
        # send_mail(
        #     subject,
        #     message,
        #     'mickeyjayblest@gmail.com',
        #     [transfer.user.email]
        # )
        messages.success(
            request, f"Transfer with id: {transfer_id} has been confirmed."
        )
    
    form = TransferSuccessForm()

    transfers = Transfer.objects.all().order_by('-dotf')
    pending_transfers = Transfer.objects.filter(is_success=False).order_by('-dotf')
    context = {
        'transfers': transfers,
        'p_transfers': pending_transfers,
        'form': form,
        'title': 'transfers'
    }
    return render(request, 'users/all_transfers.html', context)


@login_required
def update_users(request, username):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    user = get_object_or_404(
            User, username=username
        )
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        c_form = ClientUpdateForm(
            request.POST, request.FILES, instance=user.profile
        )
        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            # EMAILING 
            # subject = f"User Profile Update."
            # message = f"'success', Account has been updted for {request.user.username}."
            # sender = "mickeyjayblest@gmail.com"
            # send_mail(
            #     subject,
            #     message,
            #     'mickeyjayblest@gmail.com',
            #     [request.user.email]
            # )
            messages.success(request, f"account successfully updated")
            return redirect(
                "all_users"
            )  
    else:
        u_form = UserUpdateForm(instance=user)
        c_form = ClientUpdateForm(instance=user.profile)

    context = {"u_form": u_form, "c_form": c_form, 'title': 'update user'}
    return render(request, "users/update_user.html", context)



def change_pin(request):
    client = Client.objects.get(user = request.user)
    print(client.transfer_pin)
    if request.method == 'POST':
        form = ChangePinForm(request.POST)
        if form.is_valid():
            # check if pin and pin_again the same
            pin = form.cleaned_data['new_pin']
            pin_again = form.cleaned_data['new_pin_again'] 
            if not pin == pin_again:
                messages.error(request, f"new pin and pin again must match.")
            # check if current_pin input is same stored transfer_pin        
            if form.cleaned_data['current_pin'] ==  client.transfer_pin:
                client.transfer_pin = pin
                client.save() 
                messages.success(request, f"Transfer Pin have successfully changed.")
                send_mail(
                    "Pin change",
                    "Pin Has successfully changed.",
                    'mickeyjayblest@gmail.com',
                    ['ukejemichael@gmail.com']
                )
                return redirect(
                    "userprofile", request.user.username
                )
            else:
                messages.error(request, f"have you forgoten your pin please contact customer care.")      
    context = {
        'form': ChangePinForm,
        'title': 'change pin'
    }
    return render(request, 'users/change_pin.html', context)


def change_password(request, id):
    user = User.objects.get(id=id)
    print(user.username)
    print(request.user)
    if request.method == "POST":
        form = ChangePasswordForm(request.POST, user)
        if form.is_valid():
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password_again']
            if not password == password2:
                messages.error(request, f"password and password again must match.")
            else:
                password = make_password(password, hasher="default")
                user.password = password
                user_data = user.save()
                update_session_auth_hash(request, user_data)
                messages.success(request, "Password Has been successfully updated.")
                return redirect("userprofile", user.username)
        else:
            messages.error(request, "Fix the error.")
    else:
        form = ChangePasswordForm()

    context = {
        "title": "change password",
        'form': form
    }
    return render(request, 'users/change_password.html', context)