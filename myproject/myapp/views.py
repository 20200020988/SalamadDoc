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
from django.db.models import Count
from .utils import departments







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
def newlogin (request):
    return render(request, 'newlogin.html', {})
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
    
    secretary = request.user  # Get the currently logged-in secretary

    # Retrieve the DoctorLinksSecretary object for the secretary
    doctor_links_secretary = DoctorLinksSecretary.objects.filter(secretary_id=secretary.id).first()
    appointments = []
    
    appointments_count = 0  # Initialize the appointments count
    patients_count = 0  # Initialize the patients count

    doctor_name = None  # Initialize the doctor name
    doctor_department = None  # Initialize the doctor department


    if doctor_links_secretary:
        doctor_id = doctor_links_secretary.doctor_id
        # Retrieve the appointments linked to the doctor
        appointments = Appointment.objects.filter(doctor_id=doctor_id)
        appointments_count = Appointment.objects.filter(doctor_id=doctor_id).count()

        patients_count = (
            Appointment.objects.filter(doctor_id=doctor_id)
            .values('patient_name')
            .annotate(count=Count('patient_name', distinct=True))
            .count()
        )
        
    if doctor_links_secretary:
        doctor_id = doctor_links_secretary.doctor_id

        # Retrieve the doctor linked to the current account
        doctor = User.objects.filter(id=doctor_id).first()

        if doctor:
            doctor_name = f"{doctor.first_name} {doctor.last_name}"
            doctor_department = doctor_links_secretary.doctor_department

    context = {'appointments': appointments,
               'appointments_count': appointments_count,
               'patients_count': patients_count,
               'doctor_name': doctor_name,
               'doctor_department':doctor_department}
    
    return render(request, 'dashboardsecretary.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['secretary'])
def patientsecretary (request):
    
    secretary = request.user  # Get the currently logged-in secretary

    # Retrieve the Doct5orLinksSecretary object for the secretary
    doctor_links_secretary = DoctorLinksSecretary.objects.filter(secretary_id=secretary.id).first()
    users = []

    if doctor_links_secretary:
        doctor_id = doctor_links_secretary.doctor_id
        # Retrieve all appointments linked to the doctor
        appointments = Appointment.objects.filter(doctor_id=doctor_id)
        
        # Filter out duplicate patients
        unique_patients = set()
        for appointment in appointments:
            unique_patients.add(appointment.patient_id)
        
        # Retrieve the latest appointment for each unique patient
        for patient_id in unique_patients:
            latest_appointment = Appointment.objects.filter(doctor_id=doctor_id, patient_id=patient_id).latest('id')
            users.append(latest_appointment)

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
        doctor_department=request.POST.get('doctor_department')
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
            doctor_department = doctor_links_secretary. doctor_department
        else:
            secretary_id = None
            secretary_name = None
            doctor_department = None
            
        appointment = Appointment(
            patient_name=patient_name,
            doctor_name=doctor_name,
            doctor_department = doctor_department,
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

    doctors_with_departments = []

    for user in users:
        try:
            doctor_link_secretary = DoctorLinksSecretary.objects.get(doctor_id=user.id)
            department = doctor_link_secretary.doctor_department
        except DoctorLinksSecretary.DoesNotExist:
            department = "None"

        doctor_with_department = {
            'doctor_name': user.first_name + " " + user.last_name,
            'email':user.email,
            'department': department
        }
        doctors_with_departments.append(doctor_with_department)

    return render(request, 'alldoctors.html', {'doctors_with_departments': doctors_with_departments})

def your_view_functionallDoctorsDragDown(request):
    group_id = 3  # Replace with the desired group_id
    group = Group.objects.get(id=group_id)
    users = group.user_set.all()

    doctors_with_departments = []

    for user in users:
        try:
            doctor_link_secretary = DoctorLinksSecretary.objects.get(doctor_id=user.id)
            department = doctor_link_secretary.doctor_department
        except DoctorLinksSecretary.DoesNotExist:
            department = "None"

        doctor_with_department = {
            'user': user,
            'department': department
        }
        doctors_with_departments.append(doctor_with_department)

    context = {
        'doctors_with_departments': doctors_with_departments
    }
    return render(request, 'appointmentbook.html', context)

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
    

    doctor = request.user  # Get the currently logged-in secretary

    secretary_links_doctor = DoctorLinksSecretary.objects.filter(doctor_id=doctor.id).first()
    appointments = []

    # Call your_view_numberofdoctors function
    appointments = Appointment.objects.filter(doctor_id=request.user.id)
    appointments_count = appointments.count()

    # Get the unique user count
    unique_user_count = appointments.values('patient_name').distinct().count()
    
    secretary_name = "Not Yet Assigned"  # Initialize with an empty string

    if secretary_links_doctor:
        secretary_id = secretary_links_doctor.secretary_id

        # Retrieve the doctor linked to the current account
        secretary = User.objects.filter(id=secretary_id).first()

        if secretary:
            secretary_name = f"{secretary.first_name} {secretary.last_name}"
            
    # Prepare the context data for the template
    context = {
        
        'appointments': appointments,
        'unique_user_count': unique_user_count,
        'appointments_count':appointments_count,
        'secretary_name':secretary_name,
        
    }

    # Render the template
    return render(request, 'dashboardForDoctor.html', context)

def removeSecretary(request):
    user = request.user  # Get the current user

    doctor_links_secretary = DoctorLinksSecretary.objects.filter(doctor_id=user.id).first()
    if doctor_links_secretary:
        doctor_links_secretary.delete()
        messages.success(request, "Assigned secretary removed successfully.")
    else:
        messages.error(request, "No assigned secretary found.")

    return redirect('selectSecretary')

def selectSecretary(request):
    user = request.user  # Get the current user
    
    existing_link = DoctorLinksSecretary.objects.filter(secretary_id=user.id).exists()
    if existing_link:
        messages.error(request, "A secretary has already been linked to this account.")
        return redirect('selectSecretary')  # Redirect to the same page with an error message

    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Get the form_type value
        if form_type == 'select_secretary':
            # Process the secretary form
            secretary_id = request.POST.get('secretary_id')
            secretary_name = request.POST.get('secretary_name')
            doctor_name = request.POST.get('doctor_name')
            doctor_id = request.POST.get('doctor_id')

            # Check if the user already has a linked secretary (additional check)
            existing_link = DoctorLinksSecretary.objects.filter(doctor_id=user.id).exists()
            if existing_link:
                messages.error(request, "A secretary has already been linked to this account.")
                return redirect('selectSecretary')  # Redirect to the same page with an error message

            # Check if the list already exists for the selected secretary
            existing_link = DoctorLinksSecretary.objects.filter(secretary_id=secretary_id).exists()
            if existing_link:
                messages.error(request, "The selected secretary is already assigned to another account.")
                return redirect('selectSecretary')  # Redirect to the same page with an error message

            doctor = User.objects.get(id=doctor_id)
            doctor_name = f"{doctor.first_name} {doctor.last_name}" if doctor else ""

            secretary = User.objects.get(id=secretary_id)
            secretary_name = f"{secretary.first_name} {secretary.last_name}" if secretary else ""

            docLink = DoctorLinksSecretary(
                secretary_name=secretary_name,
                secretary_id=secretary_id,
                doctor_name=doctor_name,
                doctor_id=doctor_id,
                doctor_department=None,  # Initialize the field with None

                # Assign values to other fields as needed
            )

            docLink.save()
            messages.success(request, "Secretary linked successfully.")
            return redirect('selectSecretary')  # Redirect to the same page after successful submission

        elif form_type == 'select_department':
            # Process the department form
            doctor_department = request.POST.get('doctor_department')

            # Retrieve the existing link for the current doctor
            doctor_link = DoctorLinksSecretary.objects.filter(doctor_id=user.id).first()
            if doctor_link:
                doctor_link.doctor_department = doctor_department
                doctor_link.save()
                messages.success(request, "Department updated successfully.")
                return redirect('selectSecretary')  # Redirect to the same page after successful submission

        else:
            messages.error(request, "Invalid form submission.")
            return redirect('selectSecretary')  # Redirect to the same page with an error message

    else:
        doctor_links_secretary = DoctorLinksSecretary.objects.filter(doctor_id=user.id).first()

        if doctor_links_secretary:
            secretary_name = doctor_links_secretary.secretary_name
            doctor_name = doctor_links_secretary.doctor_name
            doctor_department = doctor_links_secretary.doctor_department  # Retrieve the assigned department

            docLink = {
                'secretary_name': secretary_name,
                'doctor_name': doctor_name,
                'doctor_department': doctor_department,  # Include the assigned department in the dictionary

            }
        else:
            docLink = None

        group_id = 4  # Replace with the desired group_id
        group = Group.objects.get(id=group_id)
        users = group.user_set.all()

        context = {
            'docLink': docLink,
            'users': users,
            'departments': departments,

        }

        return render(request, 'selectSecretary.html', context)

