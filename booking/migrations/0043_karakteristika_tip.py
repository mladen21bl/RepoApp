# Generated by Django 4.2.3 on 2023-07-23 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0042_remove_bookingpage_karakteristika_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="karakteristika",
            name="tip",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="booking.tip"
            ),
        ),
    ]
