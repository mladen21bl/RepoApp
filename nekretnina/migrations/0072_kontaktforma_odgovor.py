# Generated by Django 4.2.1 on 2023-06-13 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0071_korisnik_inbox"),
    ]

    operations = [
        migrations.AddField(
            model_name="kontaktforma",
            name="odgovor",
            field=models.CharField(blank=True, max_length=700),
        ),
    ]
