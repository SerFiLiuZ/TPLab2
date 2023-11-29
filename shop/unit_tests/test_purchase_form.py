from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product

class PurchaseViewTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=100, count=5)

    def test_purchase_view_rendering(self):
        client = Client()
        url = reverse('buy', kwargs={'product_id': self.product.id})
        response = client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '<form method="post">')
        self.assertContains(response, '<input type="hidden" value="{0}" name="product" />'.format(self.product.id))
        self.assertContains(response, '<input type="text" name="person" />')
        self.assertContains(response, '<input type="text" name="address" />')
        self.assertContains(response, '<input type="submit" value="Отправить" />')

    def test_purchase_submit(self):
        client = Client()
        url = reverse('buy', kwargs={'product_id': self.product.id})
        data = {
            'product': self.product.id,
            'person': 'test',
            'address': 'test',
        }

        response = client.post(url, data)

        self.assertEqual(response.status_code, 302)
