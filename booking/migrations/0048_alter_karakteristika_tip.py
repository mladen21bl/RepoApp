# Generated by Django 4.2.3 on 2023-07-28 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0047_rename_ime_karakteristika_name_rename_ime_tip_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="karakteristika",
            name="tip",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="karakteristike",
                to="booking.tip",
            ),
        ),
    ]
