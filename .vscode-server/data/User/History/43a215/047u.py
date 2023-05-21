from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Appointment



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

def alldoctors (request):
    return render(request, 'alldoctors.html', {})
def mybooking (request):
    return render(request, 'mybooking.html', {})   
def scheduledsession (request):
    return render(request, 'scheduledsession.html', {})
def appointmentbook (request):
    return render(request, 'appointmentbook.html', {})
def dashboardForDoctor (request):
    return render(request, 'dashboardForDoctor.html', {})
def allPatients (request):
    return render(request, 'allPatients.html', {})



def register (request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='patient') 
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username)
            
            return redirect('login')
    return render(request, 'register.html', {'form': form})

@unauthenticated_user
def loginPage (request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.groups.filter(name='patient').exists():
                return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
        
    return render(request, 'login.html', {})

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def dashboard(request):
    return render(request, 'dashboard.html', {})

@login_required(login_url=('login'))
def appointment_bookingDetails(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        doctor_name = request.POST.get('doctor_name')
        appointment_date = request.POST.get('appointment_date')
        appointment_description = request.POST.get('appointment_description')
        # Get other form fields as needed
        
        appointment = Appointment(
            patient_name=patient_name,
            doctor_name=doctor_name,
            appointment_date=appointment_date,
            appointment_description = appointment_description,
            
            # Assign values to other fields as needed
        )
        appointment.save()  # Save the appointment to the database

        return redirect('appointment_bookingDetails')  # Redirect to the same page after saving
    
    appointments = Appointment.objects.filter(patient_name=request.user)

    appointments = Appointment.objects.all()

    context = {'appointments': appointments}

    return render(request, 'mybooking.html', context)


def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('appointment_bookingDetails')  # Redirect to the page displaying the table