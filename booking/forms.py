from django import forms
from .models import BookingPage
from wagtail.fields import RichTextField
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from wagtail.images.models import Image
from multiupload.fields import MultiFileField
from wagtail.images.blocks import ImageChooserBlock

class ImageUploadForm(forms.Form):
    slike = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5, required=True)

class ImageChooserFormField(forms.ModelChoiceField):
    def __init__(self, **kwargs):
        super().__init__(queryset=Image.objects.all(), **kwargs)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email adresa')


class BookingPageForm(forms.ModelForm):
    opis = forms.CharField(widget=CKEditorWidget())
    slike = forms.ModelMultipleChoiceField(
        queryset=Image.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    

    class Meta:
        model = BookingPage
        image = ImageChooserFormField(widget=ImageChooserBlock(), required=True)
        fields = ['naziv', 'povrsina', 'cena', 'opis', 'status', 'vrsta', 'grad', 'mjesto',
                  'orjentacija', 'dvoriste', 'garaza', 'bazen', 'centralno_grijanje', 'lift', 'parking',
                  'klima', 'agent', 'slike', 'latitude', 'longitude', 'image']
