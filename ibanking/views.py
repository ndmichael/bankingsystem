from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'ibanking/index.html')

def charity(request):
    return render(request, 'ibanking/charity.html')
