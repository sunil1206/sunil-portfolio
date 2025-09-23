from django.urls import path
from . import views

urlpatterns = [
    # Main Dashboard - The homepage of the inventory system
    path('', views.dashboard, name='dashboard'),

    # Core Feature Pages
    path('alerts/', views.alert_monitor, name='alert_monitor'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('scan/', views.scan_item_view, name='scan_item'),

    # API endpoint for barcode checking via JavaScript on the scan page
    path('api/check-barcode/', views.check_barcode_api, name='check_barcode_api'),

    # Action endpoint for deleting an item from the inventory list
    path('inventory/delete/<int:item_id>/', views.delete_inventory_item, name='delete_item'),
]

