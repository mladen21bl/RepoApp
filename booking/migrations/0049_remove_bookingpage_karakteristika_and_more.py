# Generated by Django 4.2.3 on 2023-08-05 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0048_alter_karakteristika_tip"),
    ]

    operations = [
        migrations.RemoveField(model_name="bookingpage", name="karakteristika",),
        migrations.RemoveField(model_name="bookingpage", name="tip",),
        migrations.RemoveField(model_name="karakteristika", name="tip",),
        migrations.DeleteModel(name="Tip",),
    ]