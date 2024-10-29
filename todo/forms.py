from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from .models import User


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Todo

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'email', 'first_name', 'password1', 'password2']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Please enter your phone number'}),
            'username': forms.TextInput(attrs={'placeholder': 'Please enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Please enter your first name'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Please enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Please confirm your password'}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'

class CreateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        widgets = {'is_due': DateInput()}
        fields = ['title','description','is_done', 'is_due']


class UpdateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        widgets = {'is_due': DateInput()}
        fields = ['title','description','is_done', 'is_due']
