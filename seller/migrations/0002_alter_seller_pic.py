# Generated by Django 4.1.3 on 2022-12-12 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seller", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seller",
            name="pic",
            field=models.FileField(default="avtar.webp", upload_to="seller_profile"),
        ),
    ]