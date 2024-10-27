from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, DeleteView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from .forms import *
from .forms import RegisterUserForm
from .models import User

# Create your views here.


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('home')
            else:
                messages.warning(request, "Account is inactive")
        else:
            messages.info(request, "Account not found, please register")
    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, f"Acount created succesfully...")
            return redirect("signin")
        else:
            print("Something went wrong")
            messages.warning(request,"Something went wrong, try again")
    else:
        form = RegisterUserForm()
    context = {'form':form}
    return render(request, 'signup.html', context)

def home(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, f"Logged out successfully ... ")
        return redirect("home")

