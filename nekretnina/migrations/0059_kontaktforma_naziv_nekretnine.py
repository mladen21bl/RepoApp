# Generated by Django 4.2.1 on 2023-06-11 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0058_nekretnina_bazen"),
    ]

    operations = [
        migrations.AddField(
            model_name="kontaktforma",
            name="naziv_nekretnine",
            field=models.CharField(default="imeneko", max_length=255),
        ),
    ]
