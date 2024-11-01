from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginPageTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_success(self):
        # Simulate POST request for login with valid credentials
        response = self.client.post(reverse('login'), {
            'email': 'anooprnair216@gmail.com',
            'password': '1234567',
        })
        
        # Check if the user is redirected after login (HTTP 302 status code)
        self.assertEqual(response.status_code, 302)
        # Optionally check if the correct page is reached after login
        self.assertRedirects(response, reverse('dashboard'))  # Assuming user redirects to 'dashboard' after login

    def test_login_failure(self):
        # Simulate POST request with invalid credentials
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword',
        })
        
        # Check if the login fails and returns the login page (HTTP 200)
        self.assertEqual(response.status_code, 200)
        # Check if the invalid login message is in the response
        self.assertContains(response, "incorrect password.")
