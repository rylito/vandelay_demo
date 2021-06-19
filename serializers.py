from rest_framework import serializers
from vandelay.models import Address, Factory, Warehouse, Machine, Inventory, Item

class AddressSerializer(serializers.ModelSerializer):
    buildingName = serializers.CharField(source='building_name')
    streetLine1 = serializers.CharField(source='street_line_1')
    streetLine2 = serializers.CharField(source='street_line_2')
    stateProvince = serializers.CharField(source='state_province')
    zipPostalCode = serializers.CharField(source='zip_postal_code')

    class Meta:
        model = Address
        exclude = ('building_name', 'street_line_1', 'street_line_2', 'state_province', 'zip_postal_code', 'id')


class FactorySerializer(serializers.ModelSerializer):
    factoryID = serializers.IntegerField(source='pk')
    factoryName = serializers.CharField(source='factory_name')
    factoryDescription = serializers.CharField(source='factory_description')
    factoryAddress = AddressSerializer(source='address')
    factoryDetailLink = serializers.URLField(source='get_fully_qualified_url')

    class Meta:
        model = Factory
        exclude = ('factory_name', 'factory_description', 'id', 'address')


class WarehouseSerializer(serializers.ModelSerializer):
    warehouseID = serializers.IntegerField(source='pk')
    warehouseName = serializers.CharField(source='warehouse_name')
    warehouseDescription = serializers.CharField(source='warehouse_description')
    warehouseAddress = AddressSerializer(source='address')
    warehouseDetailLink = serializers.URLField(source='get_fully_qualified_url')

    class Meta:
        model = Warehouse
        exclude = ('warehouse_name', 'warehouse_description', 'id', 'address', 'items')


class MachineSerializer(serializers.ModelSerializer):
    factoryID = serializers.PrimaryKeyRelatedField(source='factory', read_only=True)
    machineID = serializers.IntegerField(source='pk')
    machineName = serializers.CharField(source='machine_name')
    machineDescription = serializers.CharField(source='machine_description')
    machineDetailLink = serializers.URLField(source='get_fully_qualified_url')

    class Meta:
        model = Machine
        exclude = ('machine_name', 'machine_description', 'id', 'factory')


class ItemSerializer(serializers.ModelSerializer):
    itemID = serializers.IntegerField(source='pk')
    itemSKU = serializers.IntegerField(source='item_sku')
    itemName = serializers.CharField(source='item_name')
    itemDescription = serializers.CharField(source='item_description')
    itemDetailLink = serializers.URLField(source='get_fully_qualified_url')

    class Meta:
        model = Item
        exclude = ('item_sku', 'item_name', 'item_description', 'id')


class InventorySerializer(serializers.ModelSerializer):
    warehouseID = serializers.PrimaryKeyRelatedField(source='warehouse', read_only=True)
    itemQuantity = serializers.IntegerField(source='item_quantity')
    inventoryDetailLink = serializers.URLField(source='get_fully_qualified_url')

    class Meta:
        model = Inventory
        exclude = ('warehouse', 'item', 'item_quantity', 'id')
