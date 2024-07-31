# Generated by Django 4.2.13 on 2024-07-20 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0002_alter_order_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="original_basket",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="order",
            name="stripe_pid",
            field=models.CharField(default="", max_length=254),
        ),
    ]
