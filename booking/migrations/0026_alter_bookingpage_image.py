# Generated by Django 4.2.1 on 2023-07-18 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0025_alter_bookingpage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookingpage",
            name="image",
            field=models.ImageField(upload_to="original_images/"),
        ),
    ]
