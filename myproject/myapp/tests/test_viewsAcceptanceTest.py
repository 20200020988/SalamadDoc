import unittest
from datetime import date, datetime
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Group
from myapp.models import Appointment, DoctorLinksSecretary
from django.contrib.messages import get_messages
from django.contrib import messages
from myapp.utils import departments
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db import connection
from myapp.views import removeSecretary
from django.contrib.auth import authenticate, login, logout


# def appointment_bookingDetails(Responsible in Handling Appointments)
# Class includes deletion of appointment.
class AppointmentBookingDetails(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='patient')
        self.user.groups.add(self.group)    

        self.appointment = Appointment.objects.create(
            patient_name='John Doe',
            doctor_name='Dr. Smith',
            appointment_date='2023-05-28',
            appointment_description='Test appointment',
            account=self.user
        )
        
    def test_appointment_booking_details_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('appointment_bookingDetails'), {
            'patient_id': self.user.id,
            'doctor_id': 1,
            'appointment_date': '2023-05-29',
            'appointment_description': 'New appointment',
            'patient_email': 'test@example.com',
            'doctor_department': 'Cardiologist'
            # Include other required fields
        })
        self.assertEqual(response.status_code, 302)  # Check if the view redirects after successful form submission
        self.assertEqual(Appointment.objects.count(), 2)  # Check if a new appointment is created
        
    def test_delete_appointment_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_appointment', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 302)  # Check if the view redirects after deleting the appointment
        self.assertEqual(Appointment.objects.count(), 0)  # Check if the appointment is deleted

# def delete_appointmentDoctors (Deletes appointments as Doctor)
class DeleteAppointmentDoctorsAcceptanceTest(TestCase):
    def setUp(self):

        # Create a doctor user
        self.doctor = User.objects.create_user(username='doctor', password='password')
        self.secretary = User.objects.create_user(username='secretary', password='password')

        # Assign the doctor and secretary to their respective groups
        doctor_group = Group.objects.create(name='Doctor')
        secretary_group = Group.objects.create(name='Secretary')
        self.doctor.groups.add(doctor_group)
        self.secretary.groups.add(secretary_group)

    def test_delete_appointmentDoctors(self):
        # Create an appointment for testing
        appointment = Appointment.objects.create(doctor_id=self.doctor.id, patient_name='John Doe', doctor_name='Dr. Smith', appointment_description='Checkup', appointment_date='2023-06-01')

        # Authenticate the doctor user
        self.client.login(username='doctor', password='password')

        # Send a POST request to delete the appointment
        delete_url = reverse('delete_appointmentDoctors', args=[appointment.id])
        response = self.client.post(delete_url)

        # Check if the response is a redirect
        self.assertRedirects(response, reverse('appointmentspagedoctors'))

        # Check if the appointment is deleted
        self.assertFalse(Appointment.objects.filter(id=appointment.id).exists())
        
# def delete_appointmentSecretary(Deletes appointments as Secretary)
class DeleteAppointmentSecretaryAcceptanceTest(TestCase):
    def setUp(self):

        # Create a secretary user
        self.doctor = User.objects.create_user(username='doctor', password='password')
        self.secretary = User.objects.create_user(username='secretary', password='password')

        # Assign the secretary and doctor to their respective groups
        doctor_group = Group.objects.create(name='Doctor')
        secretary_group = Group.objects.create(name='Secretary')
        self.doctor.groups.add(doctor_group)
        self.secretary.groups.add(secretary_group)

    def test_delete_appointmentSecretary(self):
        # Create an appointment for testing
        appointment = Appointment.objects.create(doctor_id=self.doctor.id, patient_name='John Doe', doctor_name='Dr. Smith', appointment_description='Checkup', appointment_date='2023-06-01')

        # Authenticate the doctor user
        self.client.login(username='doctor', password='password')

        # Send a POST request to delete the appointment
        delete_url = reverse('delete_appointmentSecretary', args=[appointment.id])
        response = self.client.post(delete_url)

        # Check if the response is a redirect
        self.assertRedirects(response, reverse('appointmentspagesecretary'))

        # Check if the appointment is deleted
        self.assertFalse(Appointment.objects.filter(id=appointment.id).exists())

# def dashboardForDoctor
class DashboardForDoctorTest(TestCase):
    def setUp(self):
        # Create a doctor user
        self.doctor = User.objects.create_user(username='doctor', password='password')
        self.secretary = User.objects.create_user(username='secretary', password='password')

        # Assign the doctor and secretary to their respective groups
        doctor_group = Group.objects.create(name='Doctor')
        secretary_group = Group.objects.create(name='Secretary')
        self.doctor.groups.add(doctor_group)
        self.secretary.groups.add(secretary_group)

    def test_dashboard_for_doctor(self):
        # Create some appointments for the doctor
        Appointment.objects.create(doctor_id=self.doctor.id, patient_name='John Doe', doctor_name='Dr. Smith', appointment_description='Checkup', appointment_date='2023-06-01')
        Appointment.objects.create(doctor_id=self.doctor.id, patient_name='Jane Smith', doctor_name='Dr. Smith', appointment_description='Follow-up', appointment_date='2023-06-02')

        # Login as the doctor
        self.client.login(username='doctor', password='password')

        # Make a GET request to the dashboardForDoctor view
        response = self.client.get(reverse('dashboardForDoctor'))

        # Assert that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Assert that the appointments are present in the response context
        appointments = response.context['appointments']
        self.assertEqual(appointments.count(), 2)

        # Assert that the unique user count is correct
        unique_user_count = response.context['unique_user_count']
        self.assertEqual(unique_user_count, 2)

        # Assert that the appointments count is correct
        appointments_count = response.context['appointments_count']
        self.assertEqual(appointments_count, 2)

# def dashboardForSecretary
class DashboardSecretaryTest(TestCase):
    
    def setUp(self):
        
        self.secretary = User.objects.create_user(
            username='secretary',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )

        # Create a DoctorLinksSecretary object for the secretary
        doctor = User.objects.create_user(
            username='doctor',
            password='testpassword',
            first_name='Dr.',
            last_name='Smith'
        )
        DoctorLinksSecretary.objects.create(
            secretary_id=self.secretary.id,
            secretary_name=f"{self.secretary.first_name} {self.secretary.last_name}",
            doctor_id=doctor.id,
            doctor_name=f"{doctor.first_name} {doctor.last_name}",
            doctor_department='Cardiology'
        )

        # Create an appointment linked to the doctor
        Appointment.objects.create(
            doctor_id=doctor.id,
            patient_name='John Doe',
            doctor_name=f"{doctor.first_name} {doctor.last_name}",
            appointment_description='Checkup',
            appointment_date='2023-06-01'
        )

        # Log in as the secretary
        self.client.login(username='secretary', password='testpassword')

        # Make a GET request to the dashboardsecretary view
        url = reverse('dashboardsecretary')
        response = self.client.get(url)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert that the necessary data is present in the response context
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Dr. Smith')
        self.assertContains(response, 'Cardiology')

# def dashboard(ForPatient)
class DashboardTest(TestCase):
    def setUp(self):
        # Create a patient user
        self.user = User.objects.create_user(username='patient1', password='password')
        self.patient_group = Group.objects.create(name='patient')
        self.user.groups.add(self.patient_group)
        
        # Create the desired group with id=3
        self.desired_group = Group.objects.create(id=3, name='doctor_group')

    def test_dashboard_view(self):
        # Create doctors and assign them to the desired group
        doctor1 = User.objects.create_user(username='doctor2', password='password')
        doctor2 = User.objects.create_user(username='doctor3', password='password')
        doctor3 = User.objects.create_user(username='doctor4', password='password')
        self.desired_group.user_set.add(doctor1, doctor2, doctor3)

        # Create appointments for the patient user
        appointment1 = Appointment.objects.create(patient_name='Patient 1', patient_id='patient1', doctor_name='Doctor 1', doctor_id='doctor1', patient_email='patient1@example.com', secretary_id='secretary1', secretary_name='Secretary 1', doctor_department='Department 1', appointment_date='2023-05-30', appointment_description='Description 1', account=self.user)
        appointment2 = Appointment.objects.create(patient_name='Patient 1', patient_id='patient1', doctor_name='Doctor 2', doctor_id='doctor2', patient_email='patient1@example.com', secretary_id='secretary1', secretary_name='Secretary 1', doctor_department='Department 1', appointment_date='2023-06-02', appointment_description='Description 2', account=self.user)
        appointment3 = Appointment.objects.create(patient_name='Patient 1', patient_id='patient1', doctor_name='Doctor 3', doctor_id='doctor3', patient_email='patient1@example.com', secretary_id='secretary2', secretary_name='Secretary 2', doctor_department='Department 2', appointment_date='2023-06-05', appointment_description='Description 3', account=self.user)

        # Login as the patient user
        self.client.force_login(self.user)

        # Send a GET request to the dashboard view
        response = self.client.get(reverse('dashboard'))
                
        # Check that the view returns a 200 OK status code
        self.assertEqual(response.status_code, 200)
        
        # Check that the 'dashboard.html' template is used to render the response
        self.assertTemplateUsed(response, 'dashboard.html')
        
        # Check the context data
        self.assertEqual(response.context['user_count'], 3)  # Verify the total number of doctors in the desired group
        self.assertEqual(response.context['appointments_count'], 3)  # Verify the count of appointments made by the patient
        self.assertEqual(response.context['latest_appointment_date'], date(2023, 6, 5))


        # Check the rendered content
        self.assertContains(response, 'Total Doctor')
        self.assertContains(response, 'Total Booking')
        self.assertContains(response, 'Your latest booking is')
        self.assertContains(response, appointment3.patient_name)
        self.assertContains(response, appointment3.doctor_name)
        self.assertContains(response, appointment3.appointment_description)

# def Register
class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

        # Create the 'patient' group
        Group.objects.create(name='patient')

    def test_register(self):
        # Make a GET request to the register view
        response = self.client.get(self.register_url)

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the registration form
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')

        # Create a user registration data
        registration_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword'
            # Include other required fields here
        }

        # Make a POST request to the register view with the registration data
        response = self.client.post(self.register_url, registration_data)

        # Assert that the user is redirected to the login page
        self.assertRedirects(response, reverse('login'))

        # Assert that the user account was created
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Assert that the user is assigned to the 'patient' group
        user = User.objects.get(username='testuser')
        self.assertTrue(user.groups.filter(name='patient').exists())

        # Assert that a success message is displayed
        storage = get_messages(response.wsgi_request)
        messages_list = [m.message for m in storage]
        self.assertIn('Account was created for testuser', messages_list)

# def loginPage(ToDoctor)
class LoginPageDashboardForDoctorTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboardForDoctor')
        self.doctor_group = Group.objects.create(name='doctor')
        self.user = User.objects.create_user(
            username='testdoctor',
            password='testpassword'
        )
        self.user.groups.add(self.doctor_group)

    def test_login_authenticated_doctor(self):
        # Make a GET request to the login page
        response = self.client.get(self.login_url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Log in as a doctor user
        response = self.client.post(
            self.login_url,
            {'username': 'testdoctor', 'password': 'testpassword'}
        )

        # Assert that the user is redirected to the doctor dashboard
        self.assertRedirects(response, self.dashboard_url)

    def test_dashboard_authenticated_doctor(self):
        # Log in as a doctor user
        self.client.login(username='testdoctor', password='testpassword')

        # Make a GET request to the doctor dashboard
        response = self.client.get(self.dashboard_url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the appropriate template is used for rendering
        self.assertTemplateUsed(response, 'dashboardForDoctor.html')

# def loginPage(ToPatient)
class LoginPageDashboardForPatientTest(TestCase):
    def setUp(self):
        
        self.group = Group.objects.create(id=2)

        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboard')
        self.doctor_group = Group.objects.create(name='patient')
        self.user = User.objects.create_user(
            username='testpatient',
            password='testpassword'
        )
        self.user.groups.add(self.doctor_group)

    def test_login_authenticated_doctor(self):
        # Make a GET request to the login page
        response = self.client.get(self.login_url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Log in as a doctor user
        response = self.client.post(
            self.login_url,
            {'username': 'testpatient', 'password': 'testpassword'}
        )

        # Assert that the user is redirected to the doctor dashboard
        self.assertRedirects(response, self.dashboard_url)

    def test_dashboard_authenticated_doctor(self):
        # Log in as a doctor user
        self.client.login(username='testpatient', password='testpassword')

        # Make a GET request to the doctor dashboard
        response = self.client.get(self.dashboard_url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the appropriate template is used for rendering
        self.assertTemplateUsed(response, 'dashboard.html')
        
# def loginPage(ToSecretary)
class LoginPageDashboardSecretaryTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.dashboard_url = reverse('dashboardsecretary')
        self.secretary_group = Group.objects.create(name='secretary')
        self.user = User.objects.create_user(
            username='testsecretary',
            password='testpassword'
        )
        self.user.groups.add(self.secretary_group)

    def test_login_authenticated_secretary(self):
        # Make a GET request to the login page
        response = self.client.get(self.login_url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Log in as a secretary user
        response = self.client.post(
            self.login_url,
            {'username': 'testsecretary', 'password': 'testpassword'}
        )

        # Assert that the user is redirected to the secretary dashboard
        self.assertRedirects(response, self.dashboard_url)

    def test_dashboard_authenticated_secretary(self):
        # Log in as a secretary user
        self.client.login(username='testsecretary', password='testpassword')

        # Make a GET request to the secretary dashboard
        response = self.client.get(self.dashboard_url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the appropriate template is used for rendering
        self.assertTemplateUsed(response, 'dashboardsecretary.html')

        # Add additional assertions specific to the context and functionality of the dashboardsecretary view
        # For example, check the appointments, appointments_count, patients_count, doctor_name, etc. in the context
        # and verify that they are correctly rendered in the template.
        # You can access the context using response.context

        # Example assertions:
        appointments = response.context['appointments']
        appointments_count = response.context['appointments_count']
        patients_count = response.context['patients_count']
        doctor_name = response.context['doctor_name']
        doctor_department = response.context['doctor_department']

        # Perform additional assertions as needed based on the expected behavior of 

# def logoutUser(Account)
class LogoutUserAcceptanceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')

    def test_logout_user(self):
        # Login the user
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client.post(self.login_url, data=login_data)

        # Check if the user is authenticated
        self.assertTrue(authenticate(username='testuser', password='testpassword'))

        # Perform a GET request to logout the user
        response = self.client.get(self.logout_url)

        # Assert the response status code and redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

        # Check if the user is logged out
        self.client.logout()
        self.assertFalse(self.client.session.get('_auth_user_id'))
       
# def selectSecretary (Responsible in handling the assigning of secretaries)
class DoctorSettingsSecretaryAssigningAndDepartmentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.secretary = User.objects.create_user(username='secretary', password='secretarypassword')
        self.doctor = User.objects.create_user(username='doctor', password='doctorpassword')
        self.department = 'Cardiology'
        
        existing_entries = DoctorLinksSecretary.objects.all()


        self.client.login(username='testuser', password='testpassword')

    def test_select_secretary_form(self):
        # Simulate submitting the select secretary form
        response = self.client.post(reverse('selectSecretary'), {
            'form_type': 'select_secretary',
            'secretary_id': self.secretary.id,
            'secretary_name': f'{self.secretary.first_name} {self.secretary.last_name}',
            'doctor_name': f'{self.doctor.first_name} {self.doctor.last_name}',
            'doctor_id': self.doctor.id,
        })
        self.assertEqual(response.status_code, 302)  # Check if the form submission redirects

        # Verify that the doctor-link-secretary entry is created in the database
        doc_link = DoctorLinksSecretary.objects.filter(doctor_id=self.doctor.id).first()
        self.assertIsNotNone(doc_link)
        self.assertEqual(doc_link.secretary_id, str(self.secretary.id))
        self.assertEqual(doc_link.secretary_name, f'{self.secretary.first_name} {self.secretary.last_name}')
        self.assertEqual(doc_link.doctor_name, f'{self.doctor.first_name} {self.doctor.last_name}')
        self.assertIsNone(doc_link.doctor_department)
        
    def test_select_department_form(self):
        # Create a doctor-link-secretary entry for testing
        DoctorLinksSecretary.objects.create(
            secretary_id=self.secretary.id,
            secretary_name=f'{self.secretary.first_name} {self.secretary.last_name}',
            doctor_id=self.doctor.id,
            doctor_name=f'{self.doctor.first_name} {self.doctor.last_name}',
            doctor_department=self.department,
        )
    
            # Simulate submitting the select department form
        response = self.client.post(reverse('selectSecretary'), {
            'form_type': 'select_department',
            'doctor_department': self.department,
        })
        
        self.assertEqual(response.status_code, 302)  # Check if the form submission redirects

        doc_link = DoctorLinksSecretary.objects.filter(doctor_id=self.doctor.id).first()
        self.assertEqual(doc_link.doctor_department, self.department)

# def removeSecretary
class RemoveSecretaryAssigningAndDepartmentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.secretary = User.objects.create_user(username='secretary', password='secretarypassword')
        self.doctor_links_secretary = DoctorLinksSecretary.objects.create(
            secretary_name='Secretary Name',
            secretary_id=self.secretary.id,
            doctor_name='Doctor Name',
            doctor_id=self.user.id
        )

    def test_remove_secretary_success(self):
        request = self.factory.get(reverse('removeSecretary'))
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = removeSecretary(request)
        
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(response.url, reverse('selectSecretary'))
        self.assertEqual(messages._queued_messages[0].level_tag, 'success')
        self.assertEqual(messages._queued_messages[0].message, 'Assigned secretary removed successfully.')

        self.assertFalse(DoctorLinksSecretary.objects.filter(doctor_id=self.user.id).exists())

    def test_remove_secretary_no_secretary_found(self):
            self.doctor_links_secretary.delete()

            request = self.factory.get(reverse('removeSecretary'))
            request.user = self.user
            setattr(request, 'session', 'session')
            messages = FallbackStorage(request)
            setattr(request, '_messages', messages)

            response = removeSecretary(request)
            self.assertEqual(response.status_code, 302)  # Redirect status code
            self.assertEqual(response.url, reverse('selectSecretary'))
            self.assertEqual(messages._queued_messages[0].level_tag, 'error')
            self.assertEqual(messages._queued_messages[0].message, 'No assigned secretary found.')

# def appointment_listIfYouAreADoctor (This appointments list is for doctors)
class AppointmentListIfYouAreADoctorAcceptanceTest(TestCase):
    
    def setUp(self):
        # Create a doctor user
        self.doctor = User.objects.create_user(username='doctor', password='password')

    def test_appointment_list_if_you_are_a_doctor(self):
        
        # Authenticate the doctor user
        self.client.login(username='doctor', password='password')

        # Create an appointment for the doctor user
        appointment = Appointment.objects.create(doctor_id=self.doctor.id, patient_name='John Doe', doctor_name='Dr. Smith', appointment_description='Checkup', appointment_date='2023-06-01')

        # Send a GET request to the appointment list URL
        response = self.client.get(reverse('appointmentspagedoctors'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the appointment is present in the context
        self.assertIn(appointment, response.context['appointments'])

        # Check if the appointment details are displayed in the rendered template
        self.assertContains(response, appointment.patient_name)

# def appointment_listIfYouAreADoctorLookingForSpecificPatient (This appointments list is for doctors looking for specific patient)
class AppointmentListIfYouAreADoctorLookingForSpecificPatientTest(TestCase):
    
    def setUp(self):
        # Create a doctor user
        self.doctor = User.objects.create_user(username='doctor', password='password')

    def test_appointment_list_if_you_are_a_doctor_looking_for_specific_patient(self):
        
        # Authenticate the doctor user
        self.client.login(username='doctor', password='password')

        # Create a sample account and appointment
        selected_account_id = 1  # Replace with the desired selected account ID
        appointment = Appointment.objects.create(
            doctor_id=self.doctor.id,
            account_id=selected_account_id,
            patient_name='John Doe',
            doctor_name='Dr. Smith', appointment_description='Checkup', appointment_date='2023-06-01'
        )

        # Send a GET request to the appointment list URL with the selected account ID
        url = reverse('appointmentspagedoctorsOptions', args=[selected_account_id])
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the appointment is present in the context
        self.assertIn(appointment, response.context['appointments'])

        # Check if the appointment details are displayed in the rendered template
        self.assertContains(response, appointment.patient_name)

# def your_view_function(Responsible in displaying patinets only for Doctors)
class YourViewFunctionAcceptanceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='password1')
        self.appointment1 = Appointment.objects.create(doctor_id=self.user.id, patient_name='Jane', appointment_date='2023-05-28')
        self.appointment2 = Appointment.objects.create(doctor_id=self.user.id, patient_name='John', appointment_date='2023-06-28')
        self.appointment3 = Appointment.objects.create(doctor_id=self.user.id, patient_name='Jane', appointment_date='2023-02-07')

    def test_your_view_function(self):
        # Login with the user
        self.client.login(username='john', password='password1')

        # URL for the your_view_function
        url = reverse('allPatients')

        # Perform a GET request
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert that the HTML template is rendered
        self.assertTemplateUsed(response, 'allPatients.html')

        # Assert that the rendered HTML contains the expected patient names
        expected_names = ['Jane', 'John']
        for name in expected_names:
            self.assertContains(response, name)

        # Assert that the rendered HTML doesn't contain duplicate names
        self.assertContains(response, 'Jane', count=1)
        self.assertContains(response, 'John', count=1)

        # Assert that the rendered HTML contains the appointments of the logged-in user only
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'John')
        self.assertNotContains(response, 'Alice')

        # Assert that other appointments are not included
        self.assertNotContains(response, 'Peter')
        self.assertNotContains(response, 'Mike')

# def your_view_functionallDoctors(Responsible in displaying all doctors for Patients)
class YourViewFunctionAllDoctorsAcceptanceTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(id=3)
        
        self.doctor1 = User.objects.create_user(
            username='doctor1',
            password='testpassword',
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        
        self.doctor2 = User.objects.create_user(
            username='doctor2',
            password='testpassword',
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com'
        )

        DoctorLinksSecretary.objects.create(doctor_id=self.doctor1.id, doctor_department='Cardiology')
        DoctorLinksSecretary.objects.create(doctor_id=self.doctor2.id, doctor_department='Dermatology')

        self.group.user_set.add(self.doctor1, self.doctor2)

    def test_your_view_function_all_doctors(self):
        # URL for the your_view_functionallDoctors
        url = reverse('alldoctors')

        # Perform a GET request
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert that the HTML template is rendered
        self.assertTemplateUsed(response, 'alldoctors.html')

        # Assert that the rendered HTML contains the expected doctor names and departments
        expected_doctors = [
            {'doctor_name': 'John Doe', 'email': 'john@example.com', 'department': 'Cardiology'},
            {'doctor_name': 'Jane Smith', 'email': 'jane@example.com', 'department': 'Dermatology'}
        ]
        for doctor in expected_doctors:
            self.assertContains(response, doctor['doctor_name'])
            self.assertContains(response, doctor['email'])
            self.assertContains(response, doctor['department'])

        # Assert that the rendered HTML contains the correct number of doctors
        self.assertContains(response, 'John Doe', count=1)
        self.assertContains(response, 'Jane Smith', count=1)

        # Assert that the rendered HTML doesn't contain doctors without departments
        self.assertNotContains(response, 'None')

        # Assert that other doctors are not included
        self.assertNotContains(response, 'Alice Brown')
        self.assertNotContains(response, 'Mike Johnson')

# def your_view_functionallDoctorsDragDown(Responsible in displaying all doctors in the drop down element)
class YourViewFunctionAllDoctorsDragDownAcceptanceTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(id=3)

        self.doctor1 = User.objects.create_user(
            username='doctor1',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )

        self.doctor2 = User.objects.create_user(
            username='doctor2',
            password='testpassword',
            first_name='Jane',
            last_name='Smith'
        )

        DoctorLinksSecretary.objects.create(doctor_id=self.doctor1.id, doctor_department='Cardiology')
        DoctorLinksSecretary.objects.create(doctor_id=self.doctor2.id, doctor_department='Dermatology')

        self.group.user_set.add(self.doctor1, self.doctor2)

    def test_your_view_function_all_doctors_drag_down(self):
        # URL for the your_view_functionallDoctorsDragDown
        url = reverse('appointmentbook')

        # Perform a GET request
        response = self.client.get(url)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert that the HTML template is rendered
        self.assertTemplateUsed(response, 'appointmentbook.html')

        # Assert that the rendered HTML contains the expected options in the drop-down menu
        expected_options = [
            # + The select option on the drop down button.
            '<option value="{}" data-secretary-id="" data-doctor-department="Cardiology">John Doe | Cardiology</option>'.format(self.doctor1.id),
            '<option value="{}" data-secretary-id="" data-doctor-department="Dermatology">Jane Smith | Dermatology</option>'.format(self.doctor2.id)
        ]
        for option in expected_options:
            self.assertContains(response, option)

        # Assert that the rendered HTML contains the correct number of options
        self.assertContains(response, '<option', count=3)

        # Assert that the rendered HTML contains the select element
        self.assertContains(response, '<select')

        # Assert that the select element has the correct id and name attributes
        self.assertContains(response, 'id="exampleFormControlSelect1"')
        self.assertContains(response, 'name="doctor_id"')


if __name__ == '__main__':
    unittest.main()
    
