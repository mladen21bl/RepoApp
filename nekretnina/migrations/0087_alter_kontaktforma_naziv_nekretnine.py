# Generated by Django 4.2.1 on 2023-06-14 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0086_alter_kontaktforma_naziv_nekretnine"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kontaktforma",
            name="naziv_nekretnine",
            field=models.CharField(max_length=255),
        ),
    ]
