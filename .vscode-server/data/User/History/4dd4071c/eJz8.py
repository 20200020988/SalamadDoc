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
        
    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), render(response.request, 'contact.html', {}).content.decode('utf-8'))
        
