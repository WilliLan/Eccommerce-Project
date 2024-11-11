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


    def test_login_get_request(self):
        # Simulate a GET request
        response = self.client.get(reverse('login'))


        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


    def test_logout_redirect_to_home(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')
       
        # Ensure the user is logged in
        response = self.client.get(reverse('home'))  # Assuming 'home' is a protected view
        self.assertEqual(response.status_code, 200)


        # Perform logout
        response = self.client.post(reverse('logout'))  # Adjust 'logout' to your actual logout URL name


        # Check that the user is logged out and redirected to home
        self.assertEqual(response.status_code, 302)  # Check for redirect after logout
        self.assertRedirects(response, '/')  # Expecting to redirect to the home page


    def test_session_persistence_after_login(self):
        # Simulate a POST request with valid credentials to log in
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })


        # Check if the user is redirected to 'home' after login
        self.assertRedirects(response, reverse('home'))


        # Now simulate a GET request to another page (for example, 'profile')
        response = self.client.get(reverse('about'))  # Replace with any URL you want to test


        # Check that the response is 200 OK, meaning the user is still authenticated
        self.assertEqual(response.status_code, 200)
