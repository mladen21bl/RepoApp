# Generated by Django 4.2.1 on 2023-06-28 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0014_agent_inbox_agent_is_agent_alter_bookingpage_opis_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="korisnik",
            name="username",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
