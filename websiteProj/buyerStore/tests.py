from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import Customer
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_username = 'admin'
        self.admin_password = 'admin'
        
        self.admin_user, created = User.objects.get_or_create(
            username=self.admin_username,
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            self.admin_user.set_password(self.admin_password)
            self.admin_user.save()
        
        self.client.login(username=self.admin_username, password=self.admin_password)

    def test_admin_login_page_accessible(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_admin_user_can_login(self):
        login = self.client.login(username=self.admin_username, password=self.admin_password)
        self.assertTrue(login)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/index.html')

    def test_admin_can_access_category_list_view(self):
        response = self.client.get(reverse('admin:buyerStore_category_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/change_list.html')

    def test_admin_can_access_user_list_view(self):
        response = self.client.get(reverse('admin:auth_user_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/change_list.html')


class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="john.doe@example.com",
            password="securepassword"
        )

    def test_customer_creation(self):
        # Test that a customer is created with correct fields
        customer = Customer.objects.get(email="john.doe@example.com")
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Doe")
        self.assertEqual(customer.phone, "1234567890")
        self.assertEqual(customer.email, "john.doe@example.com")

    def test_customer_update(self):
        # Test updating the customer's information
        self.customer.first_name = "Jane"
        self.customer.save()
        updated_customer = Customer.objects.get(email="john.doe@example.com")
        self.assertEqual(updated_customer.first_name, "Jane")

    def test_customer_delete(self):
        # Test deleting the customer
        customer_id = self.customer.id
        self.customer.delete()
        with self.assertRaises(Customer.DoesNotExist):
            Customer.objects.get(id=customer_id)

    def test_customer_str_method(self):
        # Test the string representation of the customer model
        self.assertEqual(str(self.customer), "John Doe")

    def test_customer_retrieve_by_email(self):
        # Test retrieving a customer by email
        customer = Customer.objects.get(email="john.doe@example.com")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Doe")

    def test_customer_creation_invalid_email(self):
        # Test invalid email
        customer = Customer(first_name="John", last_name="Doe", phone="1234567890", email="invalidemail", password="securepassword")
        with self.assertRaises(ValidationError):
            customer.full_clean()  # This will trigger the model validation and raise an error if invalid

    def test_customer_password_encryption(self):
        raw_password = "securepassword"
        self.customer.password = make_password(raw_password)  # Manually hash the password
        self.customer.save()

        # Check if the password is hashed
        customer = Customer.objects.get(email="john.doe@example.com")
        self.assertNotEqual(customer.password, raw_password)  # Ensure password is hashed


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page_accessible(self):
        # Send a GET request to the register URL
        response = self.client.get(reverse('register'))

        # Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the register.html template is used
        self.assertTemplateUsed(response, 'register.html')
