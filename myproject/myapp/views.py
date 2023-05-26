from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from myapp.models import DoctorLinksSecretary






# Create your views here.
from .forms import CreateUserForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Appointment
from .models import DoctorLinksSecretary
from .forms import CreateUserForm
from django.core.exceptions import ObjectDoesNotExist
from django.views import View




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
    secretary = request.user  # Get the currently logged-in secretary

    # Retrieve the DoctorLinksSecretary object for the secretary
    doctor_links_secretary = DoctorLinksSecretary.objects.filter(secretary_id=secretary.id).first()
    users = []
    
    if doctor_links_secretary:
        doctor_id = doctor_links_secretary.doctor_id
        # Retrieve the appointments linked to the doctor
        users = Appointment.objects.filter(doctor_id=doctor_id)
        
    context = {'users': users}

    return render(request, 'patientsecretary.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['secretary'])
def appointmentspagesecretary (request):
    
    secretary = request.user  # Get the currently logged-in secretary

    # Retrieve the DoctorLinksSecretary object for the secretary
    doctor_links_secretary = DoctorLinksSecretary.objects.filter(secretary_id=secretary.id).first()
    appointments = []
    
    if doctor_links_secretary:
        doctor_id = doctor_links_secretary.doctor_id
        # Retrieve the appointments linked to the doctor
        appointments = Appointment.objects.filter(doctor_id=doctor_id)
        
    context = {'appointments': appointments}

    return render(request, 'appointmentspagesecretary.html', context)


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
        patient_email=request.POST.get('patient_email')
        # Get other form fields as needed
        

        doctor = User.objects.get(id=doctor_id)
        doctor_name = f"{doctor.first_name} {doctor.last_name}" if doctor else ""
        
        patient = User.objects.get(id=patient_id)
        patient_name = f"{patient.first_name} {patient.last_name}" if patient else ""


        # Get the DoctorLinksSecretary object for the selected doctor
        doctor_links_secretary = DoctorLinksSecretary.objects.filter(doctor_id=doctor_id).first()
        # Extract the secretary_id and secretary_name if available
        if doctor_links_secretary:
            secretary_id = doctor_links_secretary.secretary_id
            secretary_name = doctor_links_secretary.secretary_name
        else:
            secretary_id = None
            secretary_name = None
            
        appointment = Appointment(
            patient_name=patient_name,
            doctor_name=doctor_name,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_description = appointment_description,
            patient_email=patient_email,
            secretary_id=secretary_id,
            secretary_name = secretary_name,# Set the secretary_id value

            
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

def delete_appointmentSecretary(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()    
    return redirect('appointmentspagesecretary')  # Redirect to the page displaying the table

@login_required(login_url=('login'))
def appointment_listIfYouAreADoctor(request):
    
    # Will delete print functions if final na hahahah
    print(request.user)  # Check the user object
    print(request.user.id)  # Check the user ID
    appointments = Appointment.objects.filter(doctor_id=request.user.id)
    context = {'appointments': appointments}
    return render(request, 'appointmentspagedoctors.html', context)

@login_required(login_url=('login'))
def appointment_listIfYouAreADoctorLookingForSpecificPatient(request, selected_account_id):
    
    # Will delete print functions if final na hahahah
    print(request.user)  # Check the user object
    print(request.user.id)  # Check the user ID
    
     # Retrieve the user's ID
    doctor_id = request.user.id
    
    # Filter appointments based on doctor ID and selected account ID
    appointments = Appointment.objects.filter(doctor_id=doctor_id, account_id=selected_account_id)


    context = {'appointments': appointments}
    return render(request, 'appointmentspagedoctorsOptions.html', context)


def your_view_function(request):
    appointments = Appointment.objects.filter(doctor_id=request.user.id)
    
    # Filter out duplicate names, keeping only the last entry for each name
    unique_names = appointments.values('patient_name').annotate(latest=Max('id'))
    latest_appointments = appointments.filter(id__in=[item['latest'] for item in unique_names])
    
    
    context = {'users': latest_appointments}
    return render(request, 'allPatients.html', context)


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

    group_id = 3  # Replace with the desired group_id
    group = Group.objects.get(id=group_id)
    user_count = group.user_set.count()

    appointments = Appointment.objects.filter(account=request.user)
    appointments_count = appointments.count()

    latest_appointment_date = None
    try:
        latest_appointment = appointments.latest('appointment_date')
        latest_appointment_date = latest_appointment.appointment_date
    except ObjectDoesNotExist:
        # Handle the case when no appointments exist
        pass

    # Prepare the context data for the template
    context = {
        'user_count': user_count,
        'appointments_count': appointments_count,
        'appointments': appointments,
        'latest_appointment_date': latest_appointment_date,
    }

    return render(request, 'dashboard.html', context)

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

def selectSecretary(request):
    
    user = request.user  # Get the current user
    print(user)  # Check the user object
    print(user.id)  # Check the user ID
    print(user.email)  # Check the user email

    # Check if the user already has a linked list
    existing_link = DoctorLinksSecretary.objects.filter(secretary_id=user.id).exists()
    if existing_link:
        return HttpResponseBadRequest("You already have a linked list and cannot accept incoming lists.")

    if request.method == 'POST':
        secretary_id = request.POST.get('secretary_id')
        secretary_name = request.POST.get('secretary_name')
        doctor_name = request.POST.get('doctor_name')
        doctor_id = request.POST.get('doctor_id')
        # Get other form fields as needed

        # Check if the list already exists for the selected doctor
        existing_link = DoctorLinksSecretary.objects.filter(secretary_id=secretary_id, doctor_id=doctor_id).exists()
        if existing_link:
            return HttpResponseBadRequest("List already exists for the selected doctor.")

        doctor = User.objects.get(id=doctor_id)
        doctor_name = f"{doctor.first_name} {doctor.last_name}" if doctor else ""

        secretary = User.objects.get(id=secretary_id)
        secretary_name = f"{secretary.first_name} {secretary.last_name}" if secretary else ""

        docLink = DoctorLinksSecretary(
            secretary_name=secretary_name,
            secretary_id=secretary_id,
            doctor_name=doctor_name,
            doctor_id=doctor_id,
            # Assign values to other fields as needed
        )

        docLink.save(request=request)
        return redirect('selectSecretary')  # Redirect to the same page after saving

    group_id = 4  # Replace with the desired group_id
    group = Group.objects.get(id=group_id)
    users = group.user_set.all()

    context = {
        'users': users,
    }

    return render(request, 'selectSecretary.html', context)
