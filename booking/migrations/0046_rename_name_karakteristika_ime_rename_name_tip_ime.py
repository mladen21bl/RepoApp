# Generated by Django 4.2.3 on 2023-07-28 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0045_alter_bookingpage_slike"),
    ]

    operations = [
        migrations.RenameField(
            model_name="karakteristika", old_name="name", new_name="ime",
        ),
        migrations.RenameField(model_name="tip", old_name="name", new_name="ime",),
    ]
