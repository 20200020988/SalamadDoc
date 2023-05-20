from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm
from .decorators import unauthenticated_user


def home (request):
    return render(request, 'home.html', {})

def contact (request):
    return render(request, 'contact.html', {})

def about (request):
    return render(request, 'about.html', {})

def services (request):
    return render(request, 'services.html', {}) 

def doctors (request):
    return render(request, 'doctors.html', {})

def register (request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            User = form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
            
    return render(request, 'register.html', {'form':form}) 

def loginPage (request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
        
    return render(request, 'login.html', {})

def logoutUser(request):
    logout(request)
    return redirect('home')
