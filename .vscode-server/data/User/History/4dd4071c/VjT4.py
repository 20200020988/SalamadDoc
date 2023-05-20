import unittest
from django.test import Client
from django.urls import reverse
from django.shortcuts import render

from myapp.views import home

class HomeViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), render(response.request, 'home.html', {}).content.decode('utf-8'))
        
    def test_dashboard_view_as_patient(self):
        user = user.objects.create_user(username='testuser', password='testpassword')
        user.userprofile.role = 'patient'
        user.save()
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)