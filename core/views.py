from rest_framework import viewsets, mixins

from core import serializers
from core.models import Fruit, Size, Additional, Order


class ListFruits(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Lists fruits """

    queryset = Fruit.objects.all()
    serializer_class = serializers.FruitSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class ListSizes(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Lists sizes """

    queryset = Size.objects.all()
    serializer_class = serializers.SizeSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class ListAdditionals(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Lists additionals """

    queryset = Additional.objects.all()
    serializer_class = serializers.AdditionalSerializer

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class OrderViewSet(viewsets.ModelViewSet):
    """ Manage orders in the database """

    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        """ Create a new order """

        order = serializer.save()
        order.total_price = order.get_total_price()
        order.total_prepare_time = order.get_total_prepare_time()
        order.save()
