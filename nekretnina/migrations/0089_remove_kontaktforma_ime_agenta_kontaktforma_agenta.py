# Generated by Django 4.2.1 on 2023-06-14 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0088_kontaktforma_ime_agenta"),
    ]

    operations = [
        migrations.RemoveField(model_name="kontaktforma", name="ime_agenta",),
        migrations.AddField(
            model_name="kontaktforma",
            name="agenta",
            field=models.ForeignKey(
                default="006",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="upiti",
                to="nekretnina.agent",
            ),
        ),
    ]
