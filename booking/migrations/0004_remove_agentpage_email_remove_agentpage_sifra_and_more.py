# Generated by Django 4.2.1 on 2023-06-21 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("booking", "0003_agentindexpage_agentpage"),
    ]

    operations = [
        migrations.RemoveField(model_name="agentpage", name="email",),
        migrations.RemoveField(model_name="agentpage", name="sifra",),
        migrations.RemoveField(model_name="agentpage", name="telefon",),
        migrations.RemoveField(model_name="agentpage", name="user",),
        migrations.RemoveField(model_name="agentpage", name="username",),
        migrations.CreateModel(
            name="Agent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(default="kevin", max_length=255, unique=True),
                ),
                ("sifra", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("telefon", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        default="",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="agentpage",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="booking.agent",
            ),
        ),
    ]
