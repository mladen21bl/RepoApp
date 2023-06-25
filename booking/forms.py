from django import forms
from .models import BookingPage
from wagtail.fields import RichTextField

class BookingPageForm(forms.ModelForm):

    class Meta:
        model = BookingPage
        fields = ['naziv', 'povrsina', 'cena', 'opis', 'status', 'vrsta', 'grad', 'mjesto',
                  'dvoriste', 'garaza', 'bazen', 'centralno_grijanje', 'lift', 'parking', 'klima',
                  'agent']
