from django.test import TestCase, Client
from django.urls import reverse
from django.db import models
from shop.models import Product, Purchase
from shop.views import PurchaseCreate

class ProductViewsTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100, count=5)

    def test_index_view(self):
        client = Client()
        response = client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_purchase_create_view(self):
        client = Client()
        response = client.get(reverse('buy', args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Покупка')

    def test_purchase_create_post(self):
        client = Client()
        purchase_data = {
            'product': self.product.id,
            'person': 'test',
            'address': 'test1'
        }

        response = client.post(reverse('buy', args=[self.product.id]), purchase_data, follow=True)

        self.assertEqual(response.status_code, 200)

