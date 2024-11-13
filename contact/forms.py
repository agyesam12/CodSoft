from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User,Contact

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

class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'location', 'email', 'phone_number', 'message', 'save_to', 'has_whatsapp']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Please enter the firstname'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Please enter the last name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Please enter the location'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Please enter the phone number'}),
            'message': forms.Textarea(attrs={'placeholder': 'Please enter any message for this contact'}),
            'save_to': forms.Select(attrs={'placeholder': 'Please select where to save'}),
            'has_whatsapp': forms.CheckboxInput(attrs={'placeholder': 'Does this contact have WhatsApp?'})
        }


class UpdateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name','last_name','location', 'email','phone_number','message','save_to','has_whatsapp']



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            
            
            'message': forms.Textarea(attrs={'place holder': 'please lets us know your feedback '})
        }

        