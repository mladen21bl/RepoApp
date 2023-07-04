# Generated by Django 4.2.1 on 2023-06-12 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("nekretnina", "0067_alter_korisnik_email_alter_korisnik_ime"),
    ]

    operations = [
        migrations.AddField(
            model_name="korisnik",
            name="user",
            field=models.OneToOneField(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
