from django.test import TestCase
from django.urls import reverse, resolve
from myapp.views import home, contact, about, services, doctors, register, dashboard, alldoctors, mybooking, scheduledsession, login, logout

class TestUrls(TestCase):
    def test_home_url_is_resolved(self):
        url = reverse('home')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, home)
        
    def test_contact_url_is_resolved(self):
        url = reverse('contact')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, contact)

    def test_about_url_is_resolved(self):
        url = reverse('about')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, about)

    def test_services_url_is_resolved(self):
        url = reverse('services')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, services)

    def test_doctors_url_is_resolved(self):
        url = reverse('doctors')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, doctors)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, register)

    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, dashboard)

    def test_alldoctors_url_is_resolved(self):
        url = reverse('alldoctors')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, alldoctors)

    def test_mybooking_url_is_resolved(self):
        url = reverse('mybooking')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, mybooking)

    def test_scheduledsession_url_is_resolved(self):
        url = reverse('scheduledsession')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, scheduledsession)
        
   # login and logout urls are to be tested in test_views
        
