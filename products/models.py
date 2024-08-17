from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User


class Category(models.Model):
    """Model representing a product category."""

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """Return the friendly name of the category."""
        return self.friendly_name


class Product(models.Model):
    """Model representing a product."""

    category = models.ManyToManyField("Category", related_name="products")
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    ingredients = models.TextField()
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(null=True, blank=True)
    size = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def update_rating(self):
        """Update the product's average rating based on user ratings."""
        ratings = self.ratings.all()
        if ratings.exists():
            average_rating = (
                sum(rating.value for rating in ratings) / ratings.count()
            )
            self.rating = round(average_rating, 2)
        else:
            self.rating = None
        self.save()


class Rating(models.Model):
    """Model representing a user's rating of a product."""

    product = models.ForeignKey(
        Product, related_name="ratings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"], name="rating_per_user"
            )
        ]

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} {self.value} stars"

    def save(self, *args, **kwargs):
        """Override save to update product's average rating after saving."""
        super().save(*args, **kwargs)
        self.product.update_rating()


class NutritionalFacts(models.Model):
    """Model representing nutritional facts associated with a product."""

    product = models.ForeignKey(
        Product, related_name="nutritional_facts", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Nutritional Facts"

    def __str__(self):
        return f"{self.name} - {self.product.name}"


class RelatedProduct(models.Model):
    """Model representing a product related to another product."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="related_products"
    )
    related_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="related_to"
    )

    def __str__(self):
        return f"{self.product.name} - {self.related_product.name}"


class FastFact(models.Model):
    """Model representing a fast fact about a product."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="fast_facts"
    )
    fact = models.TextField()

    def __str__(self):
        return f"{self.product.name} - {self.fact[:40]}"
