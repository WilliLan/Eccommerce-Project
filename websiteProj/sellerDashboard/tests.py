from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from sellerDashboard.models import Seller_Summary
from buyerStore.models import Product, Category
from django.conf import settings
import os
from decimal import Decimal

class SellerTests(TestCase):
    def setUp(self):
        # Create a seller user
        self.seller = User.objects.create_user(username="seller", password="password")
        self.seller.profile.account_type = "seller"
        self.seller.profile.save()
        self.seller_summary = Seller_Summary.objects.create(seller=self.seller, revenue=Decimal('1000.00'), total_orders=10, total_balance=Decimal('500.00'), withdrawals=Decimal('0.00'))

        # Create a buyer user
        self.buyer = User.objects.create_user(username="buyer", password="password")
        self.buyer.profile.account_type = "buyer"
        self.buyer.profile.save()

    def test_dashboard_valid(self):
        # Test that a seller user can access the dashboard
        # Log in as a seller
        self.client.login(username='seller', password='password')

        # Simulate a GET request
        response = self.client.get(reverse('seller_dashboard'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'seller_dashboard.html')


    def test_dashboard_invalid(self):
        # Test that a buyer user is redirected to the home page.
        # Log in as a buyer
        self.client.login(username='buyer', password='password')

        # Simulate a GET request
        response = self.client.get(reverse('seller_dashboard'))

        # Check redirection to home page
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(response.status_code, 302)

        # Check for error message in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are not allowed to view this page")


    def test_add_product_success(self):

        self.url = reverse('add_product')
        self.client.login(username="seller", password="password")
        
        # Create a category for the product
        category = Category.objects.create(name="Coffee Ground")
        
        # Use image from the project directory
        image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', 'product', 'dark_roast.jpeg')  # Adjust this path
        try:
            with open(image_path, 'rb') as img_file:
                real_image = SimpleUploadedFile(
                    'dark_roast.jpeg',
                    img_file.read(), 
                    content_type="image/jpeg" 
                )
        except Exception as e:
            print(f"Error opening image file: {e}")
            return

        # Simulate valid product data
        valid_product_data = {
            'name': 'Test Product',
            'price': Decimal('10.99'),
            'category': category.id,
            'description': 'A test product description',
            'image': real_image,
            'is_sale': True,
            'sale_price': Decimal('9.99')
        }

        # POST request with product data
        response = self.client.post(self.url, valid_product_data)

        # Debugging: Print response content if it fails
        print(response.content)

        # Verify successful redirect to the seller dashboard
        self.assertRedirects(response, reverse('seller_dashboard'))
        self.assertEqual(response.status_code, 302)

        # Verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product added successfully!")

        # Verify the product is saved in the database
        product = Product.objects.filter(name='Test Product', seller=self.seller).first()
        self.assertIsNotNone(product)
        self.assertEqual(product.description, valid_product_data['description'])
        self.assertEqual(product.price, valid_product_data['price'])
        self.assertEqual(product.sale_price, valid_product_data['sale_price'])
        self.assertEqual(product.category.name, category.name)
