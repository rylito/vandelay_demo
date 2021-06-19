from rest_framework.decorators import APIView
from rest_framework.response import Response
from vandelay.models import Address, Factory, Warehouse, Machine, Inventory, Item
from vandelay.serializers import AddressSerializer, FactorySerializer, WarehouseSerializer, MachineSerializer, InventorySerializer, ItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework import status


# list
class FactoriesView(APIView):
    def get(self, request, format=None):
        factories = Factory.objects.all()
        data = FactorySerializer(factories, many=True).data
        return Response(data)

# detail
class FactoryView(APIView):
    def get(self, request, factory_id, format=None):
        factory = get_object_or_404(Factory, pk=factory_id)
        data = FactorySerializer(factory).data
        return Response(data)


class FactoryMachinesView(APIView):
    def get(self, request, factory_id, format=None):
        factory = get_object_or_404(Factory, pk=factory_id)
        machines = factory.machine_set.all()
        data = MachineSerializer(machines, many=True).data
        return Response(data)

# list
class MachinesView(APIView):
    def get(self, request, format=None):
        machines = Machine.objects.all()
        data = MachineSerializer(machines, many=True).data
        return Response(data)

# detail
class MachineView(APIView):
    def get(self, request, machine_id, format=None):
        machine = get_object_or_404(Machine, pk=machine_id)
        data = MachineSerializer(machine).data
        return Response(data)


# list
class WarehousesView(APIView):
    def get(self, request, format=None):
        ware = Warehouse.objects.all()
        data = WarehouseSerializer(ware, many=True).data
        return Response(data)

# detail
class WarehouseView(APIView):
    def get(self, request, warehouse_id, format=None):
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
        data = WarehouseSerializer(warehouse).data
        return Response(data)


# list
class InventoryItemsView(APIView):
    authentication_classes = (BasicAuthentication,)

    def get(self, request, format=None):
        items = Item.objects.all()
        data = ItemSerializer(items, many=True).data
        return Response(data)

    def post(self, request, format=None):
        data = request.data

        #TODO validate
        sku = data['itemSKU']

        try:
            item_obj = Item.objects.get(item_sku=sku)
            return Response({'errorMsg': f'itemSKU already exists: {sku}'}, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            item_obj = Item()

        item_obj.item_sku = sku
        item_obj.item_name = data['itemName']
        item_obj.item_description = data['itemDescription']

        item_obj.save()

        data = ItemSerializer(item_obj).data

        return Response(data)

# detail
class InventoryItemView(APIView):
    authentication_classes = (BasicAuthentication,)
    
    def get(self, request, item_id, format=None):
        item = get_object_or_404(Item, pk=item_id)
        data = ItemSerializer(item).data
        return Response(data)


    def patch(self, request, item_id, format=None):
        item_obj = get_object_or_404(Item, pk=item_id)

        sku = request.data.get('itemSKU')
        if sku:
            if Item.objects.filter(item_sku=sku).exclude(pk=item_obj.pk).exists():
                return Response({'errorMsg': f'itemSKU already exists: {sku}'}, status=status.HTTP_400_BAD_REQUEST)
            item_obj.item_sku = sku

        mappings = {
            'itemDescription': 'item_description',
            'itemName': 'item_name'
        }

        for api_name, orm_prop in mappings.items():
            val = request.data.get(api_name)
            if val:
                setattr(item_obj, orm_prop, val)

        item_obj.save()

        data = ItemSerializer(item_obj).data
        return Response(data)


class WarehouseInventoryView(APIView):
    authentication_classes = (BasicAuthentication,)

    def get(self, request, warehouse_id, format=None):
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
        warehouse_items = Inventory.objects.filter(warehouse=warehouse)

        data = []
        for inventory_item in warehouse_items:
            inventory_data = InventorySerializer(inventory_item).data
            item_data = ItemSerializer(inventory_item.item).data
            inventory_data.update(item_data)
            data.append(inventory_data)


        return Response(data)


    def put(self, request, warehouse_id, format=None):
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        # TODO validate
        item_sku = request.data['itemSKU']
        quant = request.data['itemQuantity']

        try:
            item_obj = Item.objects.get(item_sku=item_sku)
        except Item.DoesNotExist:
            return Response({'errorMsg': f'No item for itemSKU: {item_sku}'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inventory_obj = Inventory.objects.get(warehouse=warehouse, item=item_obj)
        except Inventory.DoesNotExist:
            inventory_obj = Inventory(warehouse=warehouse, item=item_obj)

        inventory_obj.item_quantity = quant
        inventory_obj.save()

        inventory_data = InventorySerializer(inventory_obj).data
        item_data = ItemSerializer(item_obj).data
        inventory_data.update(item_data)

        return Response(inventory_data)



class WarehouseInventoryDetailView(APIView):
    authentication_classes = (BasicAuthentication,)

    def get(self, request, warehouse_id, item_id, format=None):
        inventory_item = get_object_or_404(Inventory, warehouse=warehouse_id, item=item_id)

        inventory_data = InventorySerializer(inventory_item).data
        item_data = ItemSerializer(inventory_item.item).data
        inventory_data.update(item_data)
        return Response(inventory_data)


    def delete(self, request, warehouse_id, item_id, format=None):
        inventory_item = get_object_or_404(Inventory, warehouse=warehouse_id, item=item_id)
        inventory_item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
