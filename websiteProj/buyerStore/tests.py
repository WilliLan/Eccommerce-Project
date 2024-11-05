from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages

class LoginUserTest(TestCase):
    def setUp(self):
        # Create a test user for login
        self.user = User.objects.create_user(username='testuser', password='testpass')
        


    def test_login_success(self):
        # Simulate a POST request with valid credentials
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })

        # Check if the user is redirected to 'home'
        self.assertRedirects(response, reverse('home'))

        # Retrieve messages and assert
        messages_list = list(get_messages(response.wsgi_request))
        print(messages_list)  # Check what messages are retrieved
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "You Have Been Logged In")
        self.assertEqual(messages_list[0].tags, 'success')

    def test_login_failure(self):
        # Simulate a POST request with invalid credentials
        response = self.client.post(reverse('login'), {
            'username': 'joe',
            'password': 'testuse'
        })

        # Check if the user is redirected back to 'login'
        self.assertRedirects(response, reverse('login'))

        # Retrieve messages and assert
        messages_list = list(get_messages(response.wsgi_request))
        print(messages_list)  # Check what messages are retrieved
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].message, "Either your email or password was incorrect. Try again please!")
        self.assertEqual(messages_list[0].tags, 'error')

    def test_login_get_request(self):
        # Simulate a GET request
        response = self.client.get(reverse('login'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')