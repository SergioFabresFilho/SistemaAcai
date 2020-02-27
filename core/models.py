from django.db import models


class OrderOption(models.Model):
    """ Parent class for the order optionals """

    name = models.CharField(max_length=255)
    price = models.FloatField()
    prepare_time = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False) -> None:
        self.is_active = False
        self.save()

    class Meta:
        abstract = True


class Fruit(OrderOption):
    class Meta:
        db_table = 'fruits'


class Size(OrderOption):
    class Meta:
        db_table = 'sizes'


class Additional(OrderOption):
    class Meta:
        db_table = 'additionals'


class Order(models.Model):
    fruit = models.ForeignKey(Fruit, on_delete=models.DO_NOTHING)
    size = models.ForeignKey(Size, on_delete=models.DO_NOTHING)
    additionals = models.ManyToManyField(Additional)
    total_prepare_time = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)

    def get_total_prepare_time(self):
        prepare_time = self.fruit.prepare_time + self.size.prepare_time

        for additional in self.additionals.all():
            prepare_time += additional.prepare_time

        return prepare_time

    def get_total_price(self):
        price = self.fruit.price + self.size.price

        for additional in self.additionals.all():
            price += additional.price

        return price

    class Meta:
        db_table = 'orders'
