from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, InventoryItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin view for the Product model.
    """
    list_display = ('name', 'barcode')
    search_fields = ('name', 'barcode')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """
    Admin view for the InventoryItem model.
    Allows for easy management of inventory.
    """
    list_display = ('product', 'quantity', 'expiry_date', 'category', 'rack_zone', 'added_at')
    search_fields = ('product__name', 'product__barcode', 'category', 'rack_zone')
    list_filter = ('expiry_date', 'category')
    date_hierarchy = 'expiry_date'
