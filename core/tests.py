from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from .views import Home, About, Contact, SignUp, LogIn, ChangePassword, LogOut, SendMail

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        print('SetUp Done...')

    def test_home_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        
        request = self.factory.get('/')
        request.user = user

        response = Home(request)

        self.assertEqual(response.status_code, 200)
        print('Test Case 1 Pass...')

    def test_about_view(self):
        user = User.objects.create_user(username='testuser', password='12345')

        request = self.factory.get('/about/')
        request.user = user

        response = About(request)

        self.assertEqual(response.status_code, 200)
        print('Test Case 2 Pass...')

    def test_contact_view(self):
        request = self.factory.get('/contact/')
        request.user = User.objects.create(username='testuser', email='test@example.com')

        response = Contact(request)

        self.assertEqual(response.status_code, 200)
        print('Test Case 3 Pass...')

    def test_signup_view(self):
        user = User.objects.create_user(username='testuser', password='12345')

        request = self.factory.get('/signup/')
        request.user = user
        
        response = SignUp(request)

        self.assertEqual(response.status_code, 302)
        print('Test Case 4 Pass...')

    def test_login_view(self):
        user = User.objects.create_user(username='testuser', password='12345')

        request = self.factory.get('/login/')
        request.user = user
        
        response = LogIn(request)
        
        self.assertEqual(response.status_code, 302)
        print('Test Case 5 Pass...')

    def test_change_password_view(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.force_login(user)

        request = self.factory.get('/change_password/')
        request.user = user

        response = ChangePassword(request)

        self.assertEqual(response.status_code, 200)
        print('Test Case 6 Pass...')

    def test_logout_view(self):
        user = User.objects.create_user(username='testuser', password='12345')

        request = self.factory.get('/logout/')
        request.user = user

        response = LogOut(request)
        
        self.assertEqual(response.status_code, 302)  # Redirects to homepage
        print('Test Case 7 Pass...')

    def test_send_mail_view(self):
        request = self.factory.get('/send_mail/')

        response = SendMail(request)

        self.assertEqual(response.status_code, 302)  # Redirects to /contact/
        print('Test Case 8 Pass...')
