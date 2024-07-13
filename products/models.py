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
    

    def __str__(self):
        return self.name

class NutritionalFacts(models.Model):
    product = models.ForeignKey(Product, related_name='nutritional_facts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Nutritional Facts'

    def __str__(self):
        return f"{self.name} - {self.product.name}"

class RelatedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_products')
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_to')

    def __str__(self):
        return f"{self.product.name} - {self.related_product.name}"

class FastFact(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fast_facts')
    fact = models.TextField()

    def __str__(self):
        return f"{self.product.name} - {self.fact[:40]}"