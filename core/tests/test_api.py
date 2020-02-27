from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Fruit, Size, Additional, Order
from core.serializers import OrderSerializer, OrderDetailSerializer

FRUITS_URL = reverse('core:fruit-list')
SIZES_URL = reverse('core:size-list')
ADDITIONALS_URL = reverse('core:additional-list')
ORDERS_URL = reverse('core:order-list')


def order_detail_url(order_id):
    """ Return order detail url """
    return reverse('core:order-detail', args=[order_id])


class AcaiApiTests(TestCase):
    """ Test api endpoints """

    def setUp(self) -> None:
        self.client = APIClient()
        self.kiwi = Fruit.objects.create(
            name='Kiwi',
            price=5,
            prepare_time=10
        )
        self.medium = Size.objects.create(
            name='Médio',
            price=0,
            prepare_time=10
        )
        self.granola = Additional.objects.create(
            name='Granola',
            price=0,
            prepare_time=10
        )
        self.order = Order.objects.create(
            fruit=self.kiwi,
            size=self.medium
        )
        self.order.additionals.add(self.granola)

    def test_retrieve_fruits(self):
        """ Test retrieving fruits ok """

        Fruit.objects.create(name='Banana',
                             price=0,
                             prepare_time=0,
                             is_active=False)

        response = self.client.get(FRUITS_URL)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_sizes(self):
        """ Test retrieving sizes ok """

        Size.objects.create(name='Grande',
                            price=0,
                            prepare_time=0,
                            is_active=False)

        response = self.client.get(SIZES_URL)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_additionals(self):
        """ Test retrieving additionals ok """

        Additional.objects.create(name='Leite Ninho',
                                  price=0,
                                  prepare_time=0,
                                  is_active=False)

        response = self.client.get(ADDITIONALS_URL)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_successful(self):
        """ Test creating an order"""

        payload = {
            'fruit': self.kiwi.id,
            'size': self.medium.id,
            'additionals': [self.granola.id],
        }

        response = self.client.post(ORDERS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.get(id=response.data['id'])

        self.assertEqual(created_order.fruit, self.kiwi)
        self.assertEqual(created_order.size, self.medium)
        self.assertIn(self.granola, created_order.additionals.all())

    def test_create_order_without_additionals(self):
        """ Test creating an order without additionals """

        payload = {
            'fruit': self.kiwi.id,
            'size': self.medium.id,
        }

        response = self.client.post(ORDERS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.get(id=response.data['id'])

        self.assertEqual(created_order.fruit, self.kiwi)
        self.assertEqual(created_order.size, self.medium)

    def test_create_order_with_many_additionals(self):
        """ Test creating an order with many additionals """

        powdered_milk = Additional.objects.create(name='Leite Ninho',
                                                  price=0,
                                                  prepare_time=0)

        payload = {
            'fruit': self.kiwi.id,
            'size': self.medium.id,
            'additionals': [self.granola.id, powdered_milk.id],
        }

        response = self.client.post(ORDERS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.get(id=response.data['id'])

        self.assertEqual(created_order.fruit, self.kiwi)
        self.assertEqual(created_order.size, self.medium)
        self.assertIn(self.granola, created_order.additionals.all())
        self.assertIn(powdered_milk, created_order.additionals.all())

    def test_view_order_detail(self):
        """ Test viewing an order detail """

        serializer = OrderDetailSerializer(self.order)
        response = self.client.get(order_detail_url(self.order.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEquals(response.data['fruit'], self.kiwi)
