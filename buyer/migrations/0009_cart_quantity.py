# Generated by Django 4.1.2 on 2022-12-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0008_remove_cart_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="quantity",
            field=models.IntegerField(default=1, null=True),
        ),
    ]
