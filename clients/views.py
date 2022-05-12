from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Client
from django.contrib import messages
from .forms import ClientUpdateForm, UserUpdateForm, DeactivateUser, ClientRegisterForm, UserForm
from clients.models import Client, Transfer
from random import randrange


# Create your views here.
def profile(request, username):
    user = get_object_or_404(
        User, username=username
    )  # getting the current user passed to it
    profile = Client.objects.filter(user=user)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, 'account/profile.html', context)

def admin(request):
    return render(request, 'users/admin.html')


def register(request):
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
            messages.success(
                request, f"Account has been created for {username} you  can now login."
            )
            return redirect("all_users")
    else:
        u_form = UserForm()
        c_form = ClientRegisterForm()
    context = {
        'c_form': c_form,
        'u_form': u_form
    }
    return render(request, 'users/register.html', context)

def all_users(request):
    if request.POST:
        username = request.POST.get('id')
        # user = User.objects.get(username=username)
        user = get_object_or_404(User, username=username)
        if  request.POST.get('deactivate') == 'on':
            print(user.is_active)
            user.is_active = False
            user.save()
            print(user.is_active)
        return redirect(
                "all_users"
            )  
    else:
        deactivate_form = DeactivateUser()
    
    clients = Client.objects.all().filter(user__is_active=True)
    context = {
        'clients': clients,
        'd_form': deactivate_form
    }
    return render(request, 'users/all_users.html', context)

def all_transfers(request):
    transfers = Transfer.objects.all()
    context = {
        'transfers': transfers
    }
    return render(request, 'users/all_transfers.html', context)

def update_users(request, username):
    user = get_object_or_404(
            User, username=username
        )
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        c_form = ClientUpdateForm(
            request.POST, request.FILES, instance=user
        )
        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, f"account successfully updated")
            return redirect(
                "all_users"
            )  
    else:
        u_form = UserUpdateForm(instance=user)
        c_form = ClientUpdateForm(instance=user.profile)

    context = {"u_form": u_form, "c_form": c_form}
    return render(request, "users/update_user.html", context)