from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
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
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationFOrm(request.POST)
        if form.is_valid():
            form.save( )
            
    return render(request, 'register.html', {'form':form}) 
