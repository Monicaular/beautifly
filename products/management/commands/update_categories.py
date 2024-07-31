import json
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = "Load categories from JSON file without creating duplicates"

    def handle(self, *args, **kwargs):
        with open("products/fixtures/categories.json") as file:
            data = json.load(file)

        for item in data:
            fields = item["fields"]
            category, created = Category.objects.update_or_create(
                pk=item["pk"],
                defaults={
                    "name": fields["name"],
                    "friendly_name": fields["friendly_name"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Categories have been loaded or updated."))
