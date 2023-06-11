from django.urls import path, include
from . import views
from .views import (
    IndexView,
    NekretninaList,
    NekretninaDetailView,
    AgentiList,
    AgentiDetailView,
    kontakt_forma,
    KorisnikCreateView,
    KorisnikList,
    KorisnikDetailView,

)


app_name = 'nekretnina'

urlpatterns = [
    path('', IndexView.as_view(), name='indexview'),
    path('nekretnine/', NekretninaList.as_view(), name='nekretnina_list'),
    path('nekretnine/<int:pk>/', NekretninaDetailView.as_view(), name='nekretnina_detail'),
    path('agenti/', AgentiList.as_view(), name='agenti_list'),
    path('agenti/<int:pk>/', AgentiDetailView.as_view(), name='agenti_detail'),
    path('kontakt-forma/', kontakt_forma, name='kontakt_forma'),

    path('registracija/', KorisnikCreateView.as_view(), name='korisnik_registracija'),
    path('korisnici/<int:pk>/', KorisnikDetailView.as_view(), name='korisnik_detail'),
    path('korisnici/', KorisnikList.as_view(), name='korisnik_list'),


]
