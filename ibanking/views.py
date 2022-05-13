from django.shortcuts import render
from .forms import ContactForm

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
