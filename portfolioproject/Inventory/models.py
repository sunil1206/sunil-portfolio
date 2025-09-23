from django.db import models
from django.utils import timezone

class Product(models.Model):
    """
    Stores the core, static information about a product, including its brand.
    This data is fetched once from the API and reused.
    """
    barcode = models.CharField(max_length=100, primary_key=True, unique=True, help_text="The unique barcode (EAN/UPC) of the product.")
    name = models.CharField(max_length=255, help_text="The name of the product.")
    brand = models.CharField(max_length=150, blank=True, null=True, help_text="The brand name of the product.")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="A URL to an image of the product.")

    def __str__(self):
        return f"{self.name} ({self.brand or 'No Brand'})"

class InventoryItem(models.Model):
    """
    Represents a specific batch of a product in the inventory,
    including its location, quantity, and expiry date.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory_items")
    category = models.CharField(max_length=100, default='Uncategorized', help_text="Category of the product, e.g., Dairy, Produce.")
    rack_zone = models.CharField(max_length=100, blank=True, null=True, help_text="Location in the supermarket, e.g., Aisle 5, R3.")
    quantity = models.PositiveIntegerField(default=1, help_text="The number of units for this item batch.")
    expiry_date = models.DateField(help_text="The expiration date of this item batch.")
    added_at = models.DateTimeField(auto_now_add=True, help_text="The date and time this item was added to the inventory.")

    class Meta:
        ordering = ['expiry_date'] # Default ordering is by the soonest expiry date.

    def __str__(self):
        return f"{self.product.name} - Expires on {self.expiry_date}"

    @property
    def days_until_expiry(self):
        """Calculates the number of days until the product expires."""
        today = timezone.now().date()
        days_left = (self.expiry_date - today).days
        return days_left

    @property
    def expiry_status(self):
        """Returns a string indicating the expiry status for easy template logic."""
        days_left = self.days_until_expiry
        if days_left < 0:
            return 'expired'
        elif days_left <= 1:
            return 'urgent' # Expires today or tomorrow
        elif days_left <= 7:
            return 'soon'
        else:
            return 'safe'

