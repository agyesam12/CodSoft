from django.shortcuts import render
from .models import *

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signin(request):
    return render(request,'signin.html')

def signup(request):
    return render(request, 'signin.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
