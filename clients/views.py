from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Client
from django.contrib import messages
from .forms import ClientUpdateForm, UserUpdateForm
from clients.models import Client, Transfer


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

def all_users(request):
    if request.GET.get('post_id'):
        username = request.GET.get('post_id')
        user = get_object_or_404(
        User, username='username'
        )
    
    clients = Client.objects.all().filter(user__is_active=True)
    context = {
        'clients': clients,
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