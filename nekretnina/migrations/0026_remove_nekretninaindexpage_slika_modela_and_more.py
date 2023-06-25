# Generated by Django 4.2.1 on 2023-06-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0025_alter_nekretnina_vrsta_nekretnine"),
    ]

    operations = [
        migrations.RemoveField(model_name="nekretninaindexpage", name="slika_modela",),
        migrations.AlterField(
            model_name="nekretnina",
            name="vrsta_nekretnine",
            field=models.CharField(
                choices=[
                    ("kuca", "Kuća"),
                    ("stan", "Stan"),
                    ("vikendica", "Vikendica"),
                    ("garsonjera", "Garsonjera"),
                    ("poslovni_prostor", "Poslovni prostor"),
                ],
                default="stan",
                max_length=35,
            ),
        ),
    ]
