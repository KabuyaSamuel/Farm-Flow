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
    
    def test_password_min_length(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'pass',  # Less than minimum length
            'password2': 'pass'   # Less than minimum length
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_required_fields(self):
        form_data = {}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_required_fields(self):
        form_data = {}
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_field_attributes(self):
        form = RegisterForm()
        self.assertEqual(form.fields['first_name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['last_name'].widget.attrs['placeholder'], 'Last Name')

class LoginFormTest(TestCase):
    def test_authentication(self):
        # Create a user for authentication testing
        user = User.objects.create_user(username='johndoe', password='mypassword123')

        form_data = {
            'username': 'johndoe',
            'password': 'mypassword123',
            'remember_me': False
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

        authenticated_user = form.get_user()
        self.assertEqual(authenticated_user, user)
   
class UpdateUserFormTest(TestCase):
    def test_form_valid(self):
        user = User.objects.create(username='johndoe', email='johndoe@example.com')
        form_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
        }
        form = UpdateUserForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        user = User.objects.create(username='johndoe', email='johndoe@example.com')
        form_data = {
            'username': '',  # Invalid: Empty value
            'email': 'invalidemail',  # Invalid: Invalid email format
        }
        form = UpdateUserForm(data=form_data, instance=user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)

    def test_field_attributes(self):
        form = UpdateUserForm()
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['email'].widget.attrs['class'], 'form-control')

    def test_save_form(self):
        user = User.objects.create(username='johndoe', email='johndoe@example.com')
        form_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
        }
        form = UpdateUserForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, 'newusername')
        self.assertEqual(updated_user.email, 'newemail@example.com')
