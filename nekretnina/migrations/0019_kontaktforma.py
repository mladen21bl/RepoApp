# Generated by Django 4.2.1 on 2023-06-08 16:18

from django.db import migrations, models
import django.db.models.deletion
import wagtail.contrib.forms.models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("nekretnina", "0018_remove_kontaktformaformfield_page_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="KontaktForma",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "to_address",
                    models.CharField(
                        blank=True,
                        help_text="Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.",
                        max_length=255,
                        validators=[wagtail.contrib.forms.models.validate_to_address],
                        verbose_name="to address",
                    ),
                ),
                (
                    "from_address",
                    models.EmailField(
                        blank=True, max_length=255, verbose_name="from address"
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="subject"
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=(
                wagtail.contrib.forms.models.FormMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
    ]
