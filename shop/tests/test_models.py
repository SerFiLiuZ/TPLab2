from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime
from django.urls import reverse
from django.test import TransactionTestCase
from django.test import TestCase, TransactionTestCase
from shop.models import Product, Purchase
from datetime import datetime
from django.urls import reverse
from django.db import transaction
from shop.views import PurchaseCreate



import time

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="bracelet", price=740, count=3)
        Product.objects.create(name="chain", price=50, count=5)
        Product.objects.create(name="ring", price=1000, count=0)

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="bracelet").name, str)
        self.assertIsInstance(Product.objects.get(name="bracelet").price, int)
        self.assertIsInstance(Product.objects.get(name="bracelet").count, int)
        self.assertIsInstance(Product.objects.get(name="chain").name, str)
        self.assertIsInstance(Product.objects.get(name="chain").price, int)
        self.assertIsInstance(Product.objects.get(name="chain").count, int)
        self.assertIsInstance(Product.objects.get(name="ring").name, str)
        self.assertIsInstance(Product.objects.get(name="ring").price, int)
        self.assertIsInstance(Product.objects.get(name="ring").count, int)       

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="bracelet").price == 740)
        self.assertTrue(Product.objects.get(name="chain").price == 50)
        self.assertTrue(Product.objects.get(name="ring").price == 1000)
        self.assertTrue(Product.objects.get(name="bracelet").count == 3)
        self.assertTrue(Product.objects.get(name="chain").count == 5)
        self.assertTrue(Product.objects.get(name="ring").count == 0)

class PurchaseTestCase(TransactionTestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price=740, count=1)
        self.datetime = datetime.now()
        self.product_bracelet = Product.objects.create(name="bracelet", price=740, count=3)
        self.product_ring = Product.objects.create(name="ring", price=740, count=0)

        Purchase.objects.create(product=self.product_book,
                                person="Ivanov",
                                address="Svetlaya St.")
        
    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == self.datetime.replace(microsecond=0))
    
    def test_dec_for_db(self):
        # Получаем начальное количество продукта
        initial_count = self.product_bracelet.count

        # Вызываем функцию dec_for_db
        PurchaseCreate.dec_for_db(self.product_bracelet)

        # Обновляем продукт из базы данных
        self.product_bracelet.refresh_from_db()

        # Проверяем, что количество уменьшилось на 1
        self.assertEqual(self.product_bracelet.count, initial_count - 1)

    def test_product_list_view_with_zero_quantity(self):
        # Формируем URL для списка товаров
        url = reverse('index')

        # Отправляем GET-запрос на URL
        response = self.client.get(url)

        # Проверяем, что ответ содержит ожидаемый HTML код для товара с количеством 0
        self.assertContains(response, f'<p>Нет в наличии</p>')

        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, 200)

