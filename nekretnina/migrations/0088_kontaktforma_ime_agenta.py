# Generated by Django 4.2.1 on 2023-06-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0087_alter_kontaktforma_naziv_nekretnine"),
    ]

    operations = [
        migrations.AddField(
            model_name="kontaktforma",
            name="ime_agenta",
            field=models.CharField(default="007", max_length=255),
        ),
    ]
