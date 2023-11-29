from django.test import TestCase
from django.utils import timezone
from shop.models import Product, Purchase

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100, count=5)

    def test_product_fields(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.count, 5)

    def test_product_default_count(self):
        new_product = Product.objects.create(name="New Product", price=200)
        self.assertEqual(new_product.count, 0)

class PurchaseModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100, count=5)
        self.purchase = Purchase.objects.create(product=self.product, person="test", address="test1")

    def test_purchase_fields(self):
        self.assertEqual(self.purchase.product, self.product)
        self.assertEqual(self.purchase.person, "test")
        self.assertEqual(self.purchase.address, "test1")

    def test_purchase_date_auto_now_add(self):
        self.assertIsNotNone(self.purchase.date)
        self.assertTrue(timezone.now() - self.purchase.date < timezone.timedelta(seconds=1))
