from django.contrib import admin
from vandelay.models import Address, Factory, Machine, Warehouse, Item, Inventory

admin.site.register(Address)
admin.site.register(Factory)
admin.site.register(Machine)
admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(Inventory)
