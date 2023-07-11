from django import forms
from .models import BookingPage
from wagtail.fields import RichTextField
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from wagtail.images.models import Image




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
        fields = ['naziv', 'povrsina', 'cena', 'opis', 'status', 'vrsta', 'grad', 'mjesto',
                  'orjentacija', 'dvoriste', 'garaza', 'bazen', 'centralno_grijanje', 'lift', 'parking',
                  'klima', 'agent', 'slike', 'latitude', 'longitude']
