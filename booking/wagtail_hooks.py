from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Korisnik

class KorisnikAdmin(ModelAdmin):
    model = Korisnik
    menu_label = 'Korisnik'  # The name of the model in the admin menu
    menu_icon = 'user'  # Choose an icon from https://feathericons.com/
    menu_order = 200  # Order of the model in the admin menu
    add_to_settings_menu = False  # Exclude from Wagtail settings menu
    exclude_from_explorer = False  # Exclude from Wagtail explorer menu

    list_display = ('username', 'email', 'odobreno', 'is_agent')  # Fields to display in the admin list view
    list_filter = ('odobreno', 'is_agent')  # Add filters for these fields
    search_fields = ('username', 'email')  # Enable search on these fields

modeladmin_register(KorisnikAdmin)
