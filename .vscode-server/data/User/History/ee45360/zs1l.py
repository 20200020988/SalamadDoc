from django.test import TestCase
from django.urls import reverse, resolved
from myapp.views import home

class TestUrls(TestCase):
    
    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolved(url))
        self.assertEquals(resolved(url).func, home)