from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Korisnik

class KorisnikAdmin(ModelAdmin):
    model = Korisnik
    menu_label = 'Korisnici'  # Display name in the admin menu
    menu_icon = 'user'  # Icon name (choose from https://feathericons.com/)
    menu_order = 200  # Position in the menu
    add_to_settings_menu = False  # Add to the Settings menu
    list_display = ['username', 'email', 'odobreno']
    list_filter = ['odobreno']
    search_fields = ['username', 'email']

modeladmin_register(KorisnikAdmin)
