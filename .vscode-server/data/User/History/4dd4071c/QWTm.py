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
    

    def test_login_page_view_with_authenticated_user(self):
        # Create a test user
        username = 'testuser11'
        password = 'testpassword'
        User.objects.create_user(username=username, password=password)

        # Log in the test user
        self.client.login(username=username, password=password)

        # Access the login page view
        response = self.client.get(reverse('login'))

        # Assert that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Assert that the user is redirected to the home page
        self.assertRedirects(response, reverse('home'))