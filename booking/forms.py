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
from wagtail.images.forms import WagtailImageField
from django.forms import inlineformset_factory
from django.forms.widgets import FileInput


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email adresa')


class MultipleFileInput(forms.FileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = True

class BookingPageForm(forms.ModelForm):
    opis = forms.CharField(widget=CKEditorWidget())
    slike = forms.FileField(widget=MultipleFileInput(attrs={'accept': 'image/*'}), required=False)  # Allow multiple images

    class Meta:
        model = BookingPage
        fields = ['naziv', 'povrsina', 'cena', 'opis', 'status', 'vrsta', 'grad', 'mjesto',
                  'orjentacija', 'dvoriste', 'garaza', 'bazen', 'centralno_grijanje', 'lift', 'parking',
                  'klima', 'agent', 'latitude', 'longitude', 'slike']

BookingPageFormSet = inlineformset_factory(BookingPage, BookingPageGalleryImage, fields=('image',), extra=1)
