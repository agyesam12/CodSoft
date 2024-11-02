from django.shortcuts import render,redirect
from .models import *
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

def home(request):
    return render(request, 'home.html')

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
    return render(request,'signin.html')

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

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def signout(request):
    logout(request)
    messages.success(request,f"Logged out successfully")
    return redirect('home')

class CreateContact(LoginRequiredMixin,CreateView):
    model = Contact
    form_class = CreateContactForm
    template_name = 'create_contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'create_contacts'
        context['list_name'] = 'contactslists'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, f"contact was added successfully {self.request.user.username}")
        return reverse_lazy('ViewContacts')

class ViewContacts(LoginRequiredMixin,ListView):
    model = Contact
    template_name = 'view_contacts.html'
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'contactslists'
        context['list_name'] = 'contactslists'
        return context

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user,created_at__lt=timezone.now()).order_by('-created_at')

        
