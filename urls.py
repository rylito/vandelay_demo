from django.urls import path
from vandelay import api, views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'vandelay'

apipatterns = [
    path('factories/', api.FactoriesView.as_view(), name='factories'),
    path('factories/<int:factory_id>/', api.FactoryView.as_view(), name='factory_detail'),
    path('factories/<int:factory_id>/machines/', api.FactoryMachinesView.as_view(), name='factory_machines'),

    path('machines/', api.MachinesView.as_view(), name='machines'),
    path('machines/<int:machine_id>/', api.MachineView.as_view(), name='machine_detail'),

    path('warehouses/', api.WarehousesView.as_view(), name='warehouses'),
    path('warehouses/<int:warehouse_id>/', api.WarehouseView.as_view(), name='warehouse_detail'),
    path('warehouses/<int:warehouse_id>/inventory/', api.WarehouseInventoryView.as_view(), name='warehouse_inventory'),
    path('warehouses/<int:warehouse_id>/inventory/<int:item_id>/', api.WarehouseInventoryDetailView.as_view(), name='warehouse_inventory_detail'),

    path('inventory/items/', api.InventoryItemsView.as_view(), name='inventory_items'),
    path('inventory/items/<int:item_id>/', api.InventoryItemView.as_view(), name='inventory_item_detail'),
]

urlpatterns = format_suffix_patterns(apipatterns)

