# Generated by Django 4.2.1 on 2023-06-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0068_korisnik_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="agent",
            name="sifra",
            field=models.CharField(default="unesi_sifru", max_length=255),
        ),
    ]
