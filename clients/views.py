from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from clients.models import Client


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