import unittest
from django.test import Client
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User, Group
<<<<<<< HEAD
=======
from myapp.models import Appointment
from myapp.views import loginPage, logoutUser, dashboard, appointment_book
>>>>>>> 3b710a33d77f6dae8320a49b42ba573cdb54fd20


from myapp.views import home

class HomeViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), render(response.request, 'home.html', {}).content.decode('utf-8'))
<<<<<<< HEAD
    
=======

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_services_view(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)

    def test_doctors_view(self):
        response = self.client.get(reverse('doctors'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_alldoctors_view(self):
        response = self.client.get(reverse('alldoctors'))
        self.assertEqual(response.status_code, 200)

    def test_mybooking_view(self):
        response = self.client.get(reverse('mybooking'))
        self.assertEqual(response.status_code, 200)

    def test_scheduledsession_view(self):
        response = self.client.get(reverse('scheduledsession'))
        self.assertEqual(response.status_code, 200)

    def test_appointmentbook_view(self):
        response = self.client.get(reverse('appointmentbook'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)



>>>>>>> 3b710a33d77f6dae8320a49b42ba573cdb54fd20
