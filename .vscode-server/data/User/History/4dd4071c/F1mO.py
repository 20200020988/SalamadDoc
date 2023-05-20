import unittest
from django.test import Client
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User, Group


from myapp.views import home

class HomeViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), render(response.request, 'home.html', {}).content.decode('utf-8'))
        
    
    def test_dashboard_view_with_allowed_user(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Assign the user to the 'patient' group
        group = Group.objects.create(name='patient')
        user.groups.add(group)

        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Access the dashboard view
        response = self.client.get(reverse('dashboard'))

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected template
        self.assertTemplateUsed(response, 'dashboard.html')