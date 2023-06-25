# Generated by Django 4.2.1 on 2023-06-21 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0004_remove_agentpage_email_remove_agentpage_sifra_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="agentpage", name="agent",),
        migrations.AddField(
            model_name="agentpage",
            name="email",
            field=models.EmailField(
                default="nesto@gmail.com", max_length=254, unique=True
            ),
        ),
        migrations.AddField(
            model_name="agentpage",
            name="sifra",
            field=models.CharField(default="123", max_length=255),
        ),
        migrations.AddField(
            model_name="agentpage",
            name="telefon",
            field=models.CharField(default="065/123-456", max_length=20),
        ),
        migrations.AddField(
            model_name="agentpage",
            name="username",
            field=models.CharField(default="kevin", max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name="bookingpage",
            name="agent",
            field=models.ForeignKey(
                default="007",
                on_delete=django.db.models.deletion.CASCADE,
                to="booking.agent",
            ),
        ),
    ]
