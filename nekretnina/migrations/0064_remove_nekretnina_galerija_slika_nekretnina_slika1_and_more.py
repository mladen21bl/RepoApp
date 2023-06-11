# Generated by Django 4.2.1 on 2023-06-11 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0063_nekretnina_klima_nekretnina_parking"),
    ]

    operations = [
        migrations.RemoveField(model_name="nekretnina", name="galerija_slika",),
        migrations.AddField(
            model_name="nekretnina",
            name="slika1",
            field=models.ImageField(
                default="nekretnine_slike/berza.jpg", upload_to="nekretnine_slike/"
            ),
        ),
        migrations.AddField(
            model_name="nekretnina",
            name="slika2",
            field=models.ImageField(
                default="nekretnine_slike/berza.jpg", upload_to="nekretnine_slike/"
            ),
        ),
        migrations.AddField(
            model_name="nekretnina",
            name="slika3",
            field=models.ImageField(
                default="nekretnine_slike/berza.jpg", upload_to="nekretnine_slike/"
            ),
        ),
        migrations.AddField(
            model_name="nekretnina",
            name="slika4",
            field=models.ImageField(
                default="nekretnine_slike/berza.jpg", upload_to="nekretnine_slike/"
            ),
        ),
    ]
