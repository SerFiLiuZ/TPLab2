from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase

class ProductListViewTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name="Test Product 1", price=100, count=5)
        self.product2 = Product.objects.create(name="Test Product 2", price=200, count=0)

    def test_product_list_view_with_products(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product 1')
        self.assertContains(response, 'Test Product 2')
        self.assertContains(response, 'Купить')

    def test_product_list_view_with_zero_quantity(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product 2')
        self.assertContains(response, 'Нет в наличии')

