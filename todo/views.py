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
from .forms import RegisterUserForm,CreateTodoForm
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


class CreateTodo(LoginRequiredMixin,CreateView):
    model = Todo
    form_class = CreateTodoForm
    template_name = 'add_todo.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'add_todo'
        context['list_name'] = 'todolists'
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


    def get_success_url(self):
        messages.success(self.request, f"Todo added successfully by {self.request.user.username}")
        return reverse_lazy("ViewTodos")

class ViewTodos(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = 'todos'
    template_name = 'view_todo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'todolists'
        context['list_name'] = 'todolists'
        return context

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user, created_at__lt=timezone.now()).order_by('created_at')


class UpdateTodo(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'update_todo.html'
    form_class = UpdateTodoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'updatetodos'
        context['list_name'] = 'todoslist'
        return context

    def get_success_url(self):
        messages.success(self.request, f"Todo updated successfully by {self.request.user.username}")
        return reverse_lazy('ViewTodos')
    
    def get_object(self, queryset=None):
        try:
            return Todo.objects.get(user=self.request.user, is_done=False, pk=self.kwargs['pk'])
        except Todo.DoesNotExist:
            return None



    def form_valid(self, form):
        form.instance.user = self.request.user
        todo = Todo.objects.filter(user=form.instance.user)
        todo.update()
        return super().form_valid(form)


class DeleteTodo(LoginRequiredMixin,DeleteView):
    template_name = 'delete_todo.html'
    model = Todo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'delete_todos'
        context['list_name'] = 'todolists'
        return context

    def get_success_url(self):
        messages.success(self.request, f"Todo deleted successfully by {self.request.user.username}")
        return reverse_lazy("ViewTodos")

