from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Agent, Nekretnina, Korisnik, KontaktForma
from django.utils.safestring import SafeString

class InboxIcon(SafeString):
    def __str__(self):
        return '<span class="icon icon-site">inbox</span>'


class AgentAdmin(ModelAdmin):
    model = Agent
    menu_label = 'Agenti'
    menu_icon = InboxIcon()
    menu_order = 200
    add_to_settings_menu = False
    list_display = ['ime', 'prezime', 'email', 'inbox_count']

    def inbox_count(self, obj):
        return obj.inbox.count()

    inbox_count.short_description = 'Inbox'

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

class KontaktFormaAdmin(ModelAdmin):
    model = KontaktForma
    menu_label = 'Inbox'
    menu_icon = 'form'
    menu_order = 400
    add_to_settings_menu = False

modeladmin_register(KorisnikAdmin)
modeladmin_register(NekretninaAdmin)
modeladmin_register(AgentAdmin)
modeladmin_register(KontaktFormaAdmin)
