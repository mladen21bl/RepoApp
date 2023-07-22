# Generated by Django 4.2.1 on 2023-07-22 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0040_karakteristika_tip_remove_bookingpage_kategorije_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingpage",
            name="karakteristika",
            field=models.ManyToManyField(
                blank=True, related_name="booking_pages", to="booking.karakteristika"
            ),
        ),
        migrations.AddField(
            model_name="bookingpage",
            name="tip",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="booking_pages",
                to="booking.tip",
            ),
        ),
    ]
