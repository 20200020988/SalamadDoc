from django.test import TestCase
from django.urls import reverse, resolve
from myapp.views import home

class TestUrls(TestCase):
    
    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)