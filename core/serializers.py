from rest_framework import serializers

from core.models import Fruit, Size, Additional, Order


class OrderOptionsMeta:
    model = None
    fields = ('id', 'price', 'prepare_time', 'name')
    read_only = ('id',)


class FruitSerializer(serializers.ModelSerializer):
    """ Serializer for fruit objects """

    class Meta(OrderOptionsMeta):
        model = Fruit


class SizeSerializer(serializers.ModelSerializer):
    """ Serializer for size objects """

    class Meta(OrderOptionsMeta):
        model = Size


class AdditionalSerializer(serializers.ModelSerializer):
    """ Serializer for additional objects """

    class Meta(OrderOptionsMeta):
        model = Additional


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order objects """

    fruit = serializers.PrimaryKeyRelatedField(
        queryset=Fruit.objects.all()
    )
    size = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all()
    )
    additionals = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Additional.objects.all()
    )
    total_prepare_time = serializers.IntegerField(read_only=True, allow_null=True)
    total_price = serializers.FloatField(read_only=True, allow_null=True)

    class Meta:
        model = Order
        fields = ('id', 'fruit', 'size', 'additionals',
                  'total_prepare_time', 'total_price')
        read_only = ('id',)


class OrderDetailSerializer(OrderSerializer):
    """ Serialize an order detail """

    fruit = FruitSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    additionals = AdditionalSerializer(read_only=True, many=True)
