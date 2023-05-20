from django.test import TestCase
from django.urls import reverse, resolve
from myapp.views import home, contact, about, services, doctors, register, dashboard, alldoctors, mybooking, scheduledsession, login, logout

class TestUrls(TestCase):
    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)
        
