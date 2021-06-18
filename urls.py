from django.urls import path
from vandelay import api, views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'vandelay'

apipatterns = [
    path('factories/', api.FactoriesView.as_view(), name='factories'),
    path('factories/<int:factory_id>/', api.FactoryView.as_view(), name='factory'),
    path('factories/<int:factory_id>/machines/', api.FactoryMachinesView.as_view(), name='factory_machines'),

    path('machines/', api.MachinesView.as_view(), name='machines'),
    path('machines/<int:machine_id>/', api.MachineView.as_view(), name='machine'),

    path('warehouses/', api.WarehousesView.as_view(), name='warehouses'),
    path('warehouses/<int:warehouse_id>/', api.WarehouseView.as_view(), name='warehouse'),
    path('warehouses/<int:warehouse_id>/inventory/', api.WarehouseInventoryView.as_view(), name='warehouse_inventory'),
    path('warehouses/<int:warehouse_id>/inventory/remove/', api.WarehouseInventoryRemoveView.as_view(), name='warehouse_inventory_remove'),

    path('inventory/items/', api.InventoryItemsView.as_view(), name='inventory_items'),
    path('inventory/items/<int:item_id>/', api.InventoryItemView.as_view(), name='inventory_item'),
]

urlpatterns = format_suffix_patterns(apipatterns)

