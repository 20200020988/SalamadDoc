from django.test import TestCase
from django.test import SimpleTestCase
from myproject.forms import CreateUserForm

class CreateUserFormTestCase(TestCase):
    def test_create_user_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = CreateUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_user_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'testpassword',
            'password2': 'differentpassword',
        }
        form = CreateUserForm(data=form_data)
        self.assertFalse(form.is_valid())