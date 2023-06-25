# Generated by Django 4.2.1 on 2023-06-06 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("nekretnina", "0007_kontaktformapage_kontaktformaformfield"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nekretninapage",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="nekretnina_page",
                to="nekretnina.agent",
            ),
        ),
    ]
