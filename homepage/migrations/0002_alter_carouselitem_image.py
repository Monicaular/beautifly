# Generated by Django 4.2.13 on 2024-06-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carouselitem",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="carousel/"
            ),
        ),
    ]
