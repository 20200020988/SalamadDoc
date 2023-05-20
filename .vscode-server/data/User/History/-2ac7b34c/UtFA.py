from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
     name = forms.CharField(label='Name')
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    
