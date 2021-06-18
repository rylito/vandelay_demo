from django.db import models

class Address(models.Model):
    building_name = models.CharField(max_length=250)
    street_line_1 = models.CharField(max_length=250)
    street_line_2 = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state_province = models.CharField(max_length=250)
    zip_postal_code = models.CharField(max_length=250)
    country = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.building_name}\n{self.street_line_1}\n{self.street_line_2}\n{self.city} {self.state_province}\n{self.zip_postal_code} {self.country}'


class Factory(models.Model):
    factory_name = models.CharField(max_length=250)
    factory_description = models.TextField()
    address = models.ForeignKey('Address', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Factories'

    def __str__(self):
        return f'{self.factory_name}'


class Machine(models.Model):
    machine_name = models.CharField(max_length=250)
    machine_description = models.TextField()
    factory = models.ForeignKey('Factory', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.machine_name}'


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=250)
    warehouse_description = models.TextField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    items = models.ManyToManyField('Item', through='Inventory')

    def __str__(self):
        return f'{self.warehouse_name}'


class Item(models.Model):
    item_sku = models.CharField(max_length=250, unique=True)
    item_name = models.CharField(max_length=250)
    item_description = models.TextField()

    def __str__(self):
        return f'{self.item_name}'


class Inventory(models.Model):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    item_quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['warehouse', 'item']]
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f'{self.warehouse} - {self.item} - {self.item_quantity}'
