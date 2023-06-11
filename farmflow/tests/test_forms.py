from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, PlantImageForm
from ..models import Profile


class RegisterFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'mypassword123',
            'password2': 'mypassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'invalidemail',  # Invalid email format
            'password1': 'mypassword123',
            'password2': 'mypassword123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_password_mismatch(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'mypassword123',
            'password2': 'differentpassword'  # Passwords don't match
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)