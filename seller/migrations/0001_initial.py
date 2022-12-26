# Generated by Django 4.1.3 on 2022-12-06 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Seller",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("address", models.TextField(max_length=200)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("mobile", models.CharField(max_length=15)),
                ("password", models.CharField(max_length=50)),
                (
                    "pic",
                    models.FileField(default="avtar.webp", upload_to="seller_profile/"),
                ),
                ("dob", models.DateField(blank=True, null=True)),
                ("gender", models.CharField(max_length=10)),
            ],
        ),
    ]
