from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import (
    IndexView,
    NekretninaList,
    NekretninaDetailView,
    AgentiList,
    AgentiDetailView,
    KorisnikCreateView,
    KorisnikList,
    KorisnikDetailView,
    CustomLoginView,
    CustomLogoutView,
    AgentCreateView,
    KontaktFormaCreate,
    KontaktFormaList,
    KontaktFormaDetail,
    OdgovorView,
    NekretninaCreateView,
    NekretninaEditView,
    NekretninaDeleteView,
)


app_name = 'nekretnina'

urlpatterns = [
    path('', IndexView.as_view(), name='indexview'),
    path('nekretnine/', NekretninaList.as_view(), name='nekretnina_list'),
    path('nekretnine/create', NekretninaCreateView.as_view(), name='nekretnina_create'),
    path('nekretnine/<int:pk>/', NekretninaDetailView.as_view(), name='nekretnina_detail'),
    path('nekretnine/<int:pk>/edit', NekretninaEditView.as_view(), name='nekretnina_edit'),
    path('nekretnine/<int:pk>/delete', NekretninaDeleteView.as_view(), name='nekretnina_delete'),

    path('registracija_agent/', AgentCreateView.as_view(), name='agent_registracija'),
    path('agenti/', AgentiList.as_view(), name='agenti_list'),
    path('agenti/<int:pk>/', AgentiDetailView.as_view(), name='agenti_detail'),

    path('kontakt/', KontaktFormaCreate.as_view(), name='kontakt_forma'),
    path('upiti', KontaktFormaList.as_view(), name='upit'),
    path('upiti/<int:pk>/', KontaktFormaDetail.as_view(), name='upit_detalj'),

    path('upiti/<int:pk>/odgovor', OdgovorView.as_view(), name='odgovor'),

    path('registracija/', KorisnikCreateView.as_view(), name='korisnik_registracija'),
    path('korisnici/<int:pk>/', KorisnikDetailView.as_view(), name='korisnik_detail'),
    path('korisnici/', KorisnikList.as_view(), name='korisnik_list'),



    path('prijava/', CustomLoginView.as_view(), name='prijava'),
    path('logout/', CustomLogoutView, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
