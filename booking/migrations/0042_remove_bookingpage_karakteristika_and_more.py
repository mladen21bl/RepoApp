# Generated by Django 4.2.3 on 2023-07-23 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0041_bookingpage_karakteristika_bookingpage_tip"),
    ]

    operations = [
        migrations.RemoveField(model_name="bookingpage", name="karakteristika",),
        migrations.RemoveField(model_name="bookingpage", name="tip",),
    ]