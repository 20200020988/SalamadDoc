import unittest
from django.test import Client
from django.contrib.auth.models import User

class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        # Set up any necessary data or configurations before running the tests
        self.client = Client()

    def test_create_user_form_valid_data(self):
        # Simulate form submission with valid data and verify the expected behavior
        form_data = {
            'username': 'test1',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = self.client.post('/register.html', data=form_data)

        self.assertEqual(response.status_code, 200)  # Assuming a successful submission redirects to a success page
        self.assertEqual(User.objects.count(), 21)  # Check if a user was created
        # Add more assertions based on your application's behavior

    def test_create_user_form_invalid_data(self):
        # Simulate form submission with invalid data and verify error handling
        form_data = {
            'username': '123',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'differentpassword',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = self.client.post('/register.html', data=form_data)

        self.assertEqual(response.status_code, 200)  # Assuming invalid form data reloads the same form page
        self.assertEqual(User.objects.count(), 21)  # Check that if user was created even with invalid form data

    def test_create_user_form_missing_required_fields(self):
        # Simulate form submission with missing required fields and verify error handling
        form_data = {
            'username': 'test1',
            'email': '',  # Missing email field
            'password1': '',
            'password2': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = self.client.post('/register.html', data=form_data)

        self.assertEqual(response.status_code, 200)  # Assuming missing required fields reloads the same form page
        self.assertEqual(User.objects.count(), 21)  # Check that if user was created even with missing form data


if __name__ == '__main__':
    unittest.main()