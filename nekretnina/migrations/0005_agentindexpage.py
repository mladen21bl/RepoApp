# Generated by Django 4.2.1 on 2023-06-06 19:10

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("nekretnina", "0004_delete_agentpage"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgentIndexPage",
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
                ("intro", wagtail.fields.RichTextField(blank=True)),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
    ]
