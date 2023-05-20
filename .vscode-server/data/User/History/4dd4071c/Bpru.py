import unittest
from django.test import Client
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User


from myapp.views import home

class HomeViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), render(response.request, 'home.html', {}).content.decode('utf-8'))
        
        def test_dashboard_view_authenticated_patient(self):
        # Create a patient user
            user = User.objects.create_user(username='testuser', password='testpassword')
            user.userprofile.role = 'patient'
            user.save()

        # Log in the patient user
            self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the dashboard URL
            response = self.client.get(self.dashboard_url)

        # Assert that the response status code is 200 (success)
            self.assertEqual(response.status_code, 200)