from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.paginator import Paginator
from courses.models import Course
from users.forms import EditProfileForm
from users.views import UserHome, EditUser, DeleteUser
from django.contrib import messages

class UsersViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@example.com', password='adminpassword')
        # Create some test courses
        for i in range(10):
            Course.objects.create(name=f'Test Course {i}', description=f'Test Description {i}')

    def test_user_home_view_authenticated(self):
        request = self.factory.get(reverse('user_home'))
        request.user = self.user
        response = UserHome(request)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_user_home_view_unauthenticated(self):
        request = self.factory.get(reverse('user_home'))
        response = UserHome(request)
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(response, '/login/?next=/user/')

    def test_edit_user_view_authenticated(self):
        request = self.factory.get(reverse('edit_user', kwargs={'username': self.user.username}))
        request.user = self.user
        response = EditUser(request, username=self.user.username)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_edit_user_view_unauthenticated(self):
        request = self.factory.get(reverse('edit_user', kwargs={'username': self.user.username}))
        response = EditUser(request, username=self.user.username)
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(response, '/login/?next=/user/')

    def test_edit_user_post(self):
        form_data = {
            'username': 'newusername',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
        }
        request = self.factory.post(reverse('edit_user', kwargs={'username': self.user.username}), form_data)
        request.user = self.user
        response = EditUser(request, username=self.user.username)
        self.assertEqual(response.status_code, 302)  # Redirects after editing
        self.assertRedirects(response, '/user/')

        # Check if the user's profile has been updated
        updated_user = User.objects.get(username='newusername')
        self.assertEqual(updated_user.first_name, 'New')
        # Add more assertions as needed

    def test_delete_user_view_authenticated(self):
        request = self.factory.get(reverse('delete_user'))
        request.user = self.user
        response = DeleteUser(request)
        self.assertEqual(response.status_code, 302)  # Redirects after deleting user
        self.assertRedirects(response, '/')

        # Check if the user has been deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username=self.user.username)
        # Add more assertions as needed

    def test_delete_user_view_unauthenticated(self):
        request = self.factory.get(reverse('delete_user'))
        response = DeleteUser(request)
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(response, '/login/?next=/user/')
