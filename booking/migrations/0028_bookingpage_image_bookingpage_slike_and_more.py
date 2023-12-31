# Generated by Django 4.2.1 on 2023-07-18 21:22

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("booking", "0027_remove_bookingpage_image_remove_bookingpage_slike_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingpage",
            name="image",
            field=models.ImageField(default="stan.jpg", upload_to="original_images/"),
        ),
        migrations.AddField(
            model_name="bookingpage",
            name="slike",
            field=models.ManyToManyField(to="wagtailimages.image"),
        ),
        migrations.CreateModel(
            name="BookingPageGalleryImage",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("caption", models.CharField(blank=True, max_length=250)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="booking.bookingpage",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
    ]
