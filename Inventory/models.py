from django.db import models


class Item(models.Model):
    """
    Model representing an item in the inventory.

    Attributes:
        name (str): The name of the item.
        category (ForeignKey): The category to which the item belongs.
        quantity (int): The quantity of the item available in stock.
        price (Decimal): The price of the item.
        created_at (DateTime): Timestamp when the item was created.
        updated_at (DateTime): Timestamp when the item was last updated.
    """
    
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the name of the item as a string."""
        return self.name
