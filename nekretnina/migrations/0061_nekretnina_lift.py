# Generated by Django 4.2.1 on 2023-06-11 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0060_nekretnina_centalno_grijanje"),
    ]

    operations = [
        migrations.AddField(
            model_name="nekretnina",
            name="lift",
            field=models.BooleanField(default=False),
        ),
    ]
