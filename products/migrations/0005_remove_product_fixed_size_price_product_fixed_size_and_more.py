# Generated by Django 4.2.13 on 2024-07-06 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "products",
            "0004_product_fixed_size_price_product_has_multiple_sizes_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="fixed_size_price",
        ),
        migrations.AddField(
            model_name="product",
            name="fixed_size",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="size_options",
            field=models.TextField(blank=True, null=True),
        ),
    ]
