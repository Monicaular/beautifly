from django.db import models
from decimal import Decimal

class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Product(models.Model):
    category = models.ManyToManyField('Category', related_name='products')
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    ingredients = models.TextField()
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    nutritional_facts = models.JSONField(null=True, blank=True)
    fixed_size_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    has_multiple_sizes = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_price_for_quantity(self, quantity):
        quantity_to_kg = {
            '100g': Decimal('0.1'),
            '250g': Decimal('0.25'),
            '1kg': Decimal('1'),
        }

        price_per_kg = self.price

        if quantity in quantity_to_kg:
            quantity_in_kg = quantity_to_kg[quantity]
            total_price = round(price_per_kg * quantity_in_kg, 2)
            return total_price
        else:
            return None