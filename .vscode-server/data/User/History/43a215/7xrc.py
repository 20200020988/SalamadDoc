from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from datetime import datetime, timedelta




# Create your views here.
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Appointment
from .forms import CreateUserForm




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

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def dashboardForDoctor (request):
    return render(request, 'dashboardForDoctor.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def allPatients (request):
    return render(request, 'allPatients.html', {})  

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def appointmentspagedoctors (request):
    return render(request, 'appointmentspagedoctors.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles=['secretary'])
def dashboardsecretary (request):
    return render(request, 'dashboardsecretary.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles=['secretary'])
def patientsecretary (request):
    return render(request, 'patientsecretary.html', {})

@login_required(login_url='login')
@allowed_users(allowed_roles=['secretary'])
def appointmentspagesecretary (request):
    return render(request, 'appointmentspagesecretary.html', {})


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
            if user.groups.filter(name='doctor').exists():
                return redirect('dashboardForDoctor')
            if user.groups.filter(name='secretary').exists():
                return redirect('dashboardsecretary')
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
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        appointment_description = request.POST.get('appointment_description')
        # Get other form fields as needed
        
        doctor = User.objects.get(id=doctor_id)
        doctor_name = f"{doctor.first_name} {doctor.last_name}" if doctor else ""
        
        patient = User.objects.get(id=patient_id)
        patient_name = f"{patient.first_name} {patient.last_name}" if patient else ""


        
        appointment = Appointment(
            patient_name=patient_name,
            doctor_name=doctor_name,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_description = appointment_description,
            
            # Assign values to other fields as needed
        )
        
        appointment.save(request=request)  # Pass the request object to the save() method

        return redirect('appointment_bookingDetails')  # Redirect to the same page after saving
   
    appointments = Appointment.objects.filter(account=request.user)
    
    

    context = {'appointments': appointments}

    return render(request, 'mybooking.html', context)



def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()    
    return redirect('appointment_bookingDetails')  # Redirect to the page displaying the table

def delete_appointmentDoctors(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()    
    return redirect('appointmentspagedoctors')  # Redirect to the page displaying the table

@login_required(login_url=('login'))
def appointment_listIfYouAreADoctor(request):
    
    # Will delete print functions if final na hahahah
    print(request.user)  # Check the user object
    print(request.user.id)  # Check the user ID
    appointments = Appointment.objects.filter(doctor_id=request.user.id)
    context = {'appointments': appointments}
    return render(request, 'appointmentspagedoctors.html', context)


def your_view_function(request):
    group_id = 2  # Replace with the desired group_id
    group = Group.objects.get(id=group_id)
    users = group.user_set.all()
    return render(request, 'allPatients.html', {'users': users})


def your_view_functionallDoctors(request):
    group_id = 3  # Replace with the desired group_id
    group = Group.objects.get(id=group_id)
    users = group.user_set.all()
    return render(request, 'alldoctors.html', {'users': users})

def your_view_functionallDoctorsDragDown(request):
    group_id = 3  # Replace with the desired group_id
    group = Group.objects.get(id=group_id)
    users = group.user_set.all()
    return render(request, 'appointmentbook.html', {'users': users})

def dashboard(request):
    
    current_time = datetime.now()


    # Call your_view_numberofdoctors function
    group_id = 3  # Replace with the desired group_id
    group = Group.objects.get(id=group_id)
    user_count = group.user_set.count()
    
    appointments = Appointment.objects.filter(account=request.user)
    appointments_count = appointments.count()
    appointment_dates = [appointment.appointment_date.strftime('%B %d') for appointment in appointments]

    

    # Prepare the context data for the template
    context = {
        'user_count': user_count,
        # Other context variables
        'appointments_count': appointments_count,
                
        'appointments': appointments,
        
        'appointment_date': appointment_dates,

    }

    # Render the template
    return render(request, 'dashboard.html', context)

def dashboardForDoctor(request):
    


    # Call your_view_numberofdoctors function
    appointments = Appointment.objects.filter(doctor_id=request.user.id)

    

    # Prepare the context data for the template
    context = {
        
        'appointments': appointments,

    }

    # Render the template
    return render(request, 'dashboardForDoctor.html', context)


