# Generated by Django 4.1.3 on 2022-12-15 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seller", "0002_alter_seller_pic"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("p_name", models.CharField(max_length=30)),
                ("des", models.CharField(max_length=300)),
                ("price", models.FloatField(default=0.0)),
                ("qua", models.IntegerField(default=0)),
                ("pic", models.FileField(default="cart.png", upload_to="n_product")),
            ],
        ),
    ]
