# Generated by Django 4.2.3 on 2023-07-26 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0044_bookingpage_karakteristika_bookingpage_tip"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookingpage",
            name="slike",
            field=models.ImageField(
                default="original_images/berza.jog", upload_to="original_images/"
            ),
        ),
    ]
