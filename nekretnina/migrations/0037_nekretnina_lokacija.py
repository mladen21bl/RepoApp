# Generated by Django 4.2.1 on 2023-06-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "nekretnina",
            "0036_remove_nekretnina_bazen_remove_nekretnina_dvoriste_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="nekretnina",
            name="lokacija",
            field=models.CharField(
                choices=[
                    ("centar", "Centar"),
                    ("mejdan", "Mejdan"),
                    ("novavaros", "Nova Varos"),
                    ("borik", "Borik"),
                    ("cokori", "Cokorska Polja"),
                    ("slatina", "Slatina"),
                ],
                default="centar",
                max_length=15,
            ),
        ),
    ]
