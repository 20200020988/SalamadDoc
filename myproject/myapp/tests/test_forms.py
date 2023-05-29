import unittest
from django.test import Client
from myapp.forms import CreateUserForm
from django.contrib.auth.models import User


class TestForms(unittest.TestCase):
    def test_create_user_form_valid_data(self):
        # Create a unique username for testing
        username = 'testuser123'

        # Check if a user with the given username already exists
        if User.objects.filter(username=username).exists():
            # If a user exists, delete it
            User.objects.get(username=username).delete()

        form_data = {
            'username': username,
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = CreateUserForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())