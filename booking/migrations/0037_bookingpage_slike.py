# Generated by Django 4.2.1 on 2023-07-21 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("booking", "0036_remove_bookingpage_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingpage",
            name="slike",
            field=models.ManyToManyField(to="wagtailimages.image"),
        ),
    ]
