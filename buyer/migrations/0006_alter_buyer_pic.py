# Generated by Django 4.1.3 on 2022-12-15 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0005_alter_buyer_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyer",
            name="pic",
            field=models.FileField(
                default="avtar.webp", null=True, upload_to="profile"
            ),
        ),
    ]