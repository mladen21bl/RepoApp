from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Agent, Nekretnina, Korisnik
from django.utils.safestring import mark_safe

class AgentAdmin(ModelAdmin):
    model = Agent
    menu_label = 'Agenti'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ['ime', 'prezime', 'email']

class NekretninaAdmin(ModelAdmin):
    model = Nekretnina
    menu_label = 'Nekretnine'
    menu_icon = 'home'
    menu_order = 201
    add_to_settings_menu = False

class KorisnikAdmin(ModelAdmin):
    model = Korisnik
    menu_label = 'Zahtjevi za registraciju'
    menu_icon = 'user'
    menu_order = 300
    add_to_settings_menu = False
    list_display = ['ime', 'email', 'odobreno']
    list_filter = ['odobreno']
    search_fields = ['ime', 'email']

modeladmin_register(KorisnikAdmin)
modeladmin_register(NekretninaAdmin)
modeladmin_register(AgentAdmin)
