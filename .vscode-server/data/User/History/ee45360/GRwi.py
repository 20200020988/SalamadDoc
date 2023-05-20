from django.test import TestCase
from django.urls import reverse, resolve
from myapp.views import home, contact, about, services, doctors, register, dashboard, alldoctors, mybooking, scheduledsession, login

class TestUrls(TestCase):
    
    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)
        
    def test_contact_url_is_resolved(self):
        url = reverse('contact')
        print(resolve(url))
        self.assertEquals(resolve(url).func, contact)
        
    def test_about_url_is_resolved(self):
        url = reverse('about')
        print(resolve(url))
        self.assertEquals(resolve(url).func, about)
        
    def test_services_url_is_resolved(self):
        url = reverse('services')
        print(resolve(url))
        self.assertEquals(resolve(url).func, services)
        
    def test_doctors_url_is_resolved(self):
        url = reverse('doctors')
        print(resolve(url))
        self.assertEquals(resolve(url).func, doctors)
        
    def test_register_url_is_resolved(self):
        url = reverse('register')
        print(resolve(url))
        self.assertEquals(resolve(url).func, register)
        
    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, dashboard)
        
    def test_alldoctors_url_is_resolved(self):
        url = reverse('alldoctors')
        print(resolve(url))
        self.assertEquals(resolve(url).func, alldoctors)
        
    def test_mybooking_url_is_resolved(self):
        url = reverse('mybooking')
        print(resolve(url))
        self.assertEquals(resolve(url).func, mybooking)
        
    def test_scheduledsession_url_is_resolved(self):
        url = reverse('scheduledsession')
        print(resolve(url))
        self.assertEquals(resolve(url).func, scheduledsession)
        
    def test_login_url_is_resolved(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, login)
        