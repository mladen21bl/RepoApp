from django import forms
from .models import BookingPage, BookingPageGalleryImage
from wagtail.fields import RichTextField
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from wagtail.images.models import Image
from multiupload.fields import MultiFileField
from wagtail.images.blocks import ImageChooserBlock
from django.forms import inlineformset_factory
from wagtail.images.models import Image as WagtailImage
from wagtail.images.widgets import AdminImageChooser

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email adresa')


class BookingPageForm(forms.ModelForm):
    opis = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = BookingPage
        fields = ['naziv', 'povrsina', 'cena', 'opis', 'status', 'vrsta', 'grad', 'mjesto',
                  'orjentacija', 'dvoriste', 'garaza', 'bazen', 'centralno_grijanje', 'lift', 'parking',
                  'klima', 'agent', 'latitude', 'longitude', 'slike']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['slike'].widget = forms.ClearableFileInput(attrs={'multiple': True})
