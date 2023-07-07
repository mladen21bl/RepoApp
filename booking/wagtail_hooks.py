from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Korisnik, Poruke

class KorisnikAdmin(ModelAdmin):
    model = Korisnik
    menu_label = 'Korisnik'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False

    list_display = ('username', 'email', 'odobreno', 'is_agent')
    list_filter = ('odobreno', 'is_agent')
    search_fields = ('username', 'email')


class PorukeAdmin(ModelAdmin):
    model = Poruke
    menu_label = 'Poruke'
    menu_icon = 'mail'
    list_display = ('ime', 'tekst', 'forma')

modeladmin_register(PorukeAdmin)
modeladmin_register(KorisnikAdmin)
