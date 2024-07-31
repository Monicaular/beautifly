import json
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Product, Category, NutritionalFacts


class Command(BaseCommand):
    help = "Load nutritional facts for products from JSON file without duplicating products"

    def handle(self, *args, **kwargs):
        with open("products/fixtures/products.json") as file:
            data = json.load(file)

        for item in data:
            fields = item["fields"]
            categories = fields.pop("category", [])
            nutritional_facts = fields.pop("nutritional_facts", {})

            # Find the product by SKU
            product = Product.objects.filter(sku=fields["sku"]).first()

            if product:
                # Update product fields
                product.name = fields["name"]
                product.description = fields["description"]
                product.price = Decimal(fields["price"])
                product.ingredients = fields["ingredients"]
                product.rating = Decimal(fields["rating"])
                product.image = fields["image"]
                product.save()

                # Clear existing categories and add new ones
                product.category.clear()
                for category_id in categories:
                    category = Category.objects.get(pk=category_id)
                    product.category.add(category)

                # Clear existing nutritional facts
                product.nutritional_facts.all().delete()

                # Add new nutritional facts
                for fact_name, fact_amount in nutritional_facts.items():
                    if fact_amount is not None:
                        NutritionalFacts.objects.create(
                            product=product,
                            name=fact_name.capitalize(),
                            amount=fact_amount,
                            unit=(
                                "g"
                                if fact_name
                                in [
                                    "fat",
                                    "carbohydrates",
                                    "sugars",
                                    "fiber",
                                    "protein",
                                    "salt",
                                ]
                                else "kcal"
                            ),
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updated {product.name} with nutritional facts."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product with SKU {fields["sku"]} not found.')
                )
