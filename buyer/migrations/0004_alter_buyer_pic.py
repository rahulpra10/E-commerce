# Generated by Django 4.1.3 on 2022-12-13 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0003_alter_buyer_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buyer",
            name="pic",
            field=models.FileField(default="avtar.webp", upload_to="profile/"),
        ),
    ]