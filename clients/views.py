from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Client
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
    clients = Client.objects.all().filter(user__is_active=True)
    context = {
        'clients': clients
    }
    return render(request, 'users/all_users.html', context)

def all_transfers(request):
    transfers = Transfer.objects.all()
    context = {
        'transfers': transfers
    }
    return render(request, 'users/all_transfers.html', context)