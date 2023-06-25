from django.db import models
<<<<<<< HEAD
=======

>>>>>>> f2079d21f8d69e5e8c102949a7b7ea2cda6ff006
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
