from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    IndexView,
    AgentiList,
    AgentiDetailView,
    AgentCreateView,
    KorisnikCreateView,
    KorisnikList,
    KorisnikDetailView,
    CustomLoginView,
    CustomLogoutView,
    KontaktFormaCreate,
    KontaktFormaList,
    KontaktFormaDetail,
    OdgovorView,
    NekretninaList,
    BookingDetail,
    ForgotView,
    VerificationSuccessView,
    BookingCreateView,
    BookingDeleteView,
)


app_name = 'booking'

urlpatterns = [
    path('', IndexView.as_view(), name='indexview'),
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


    path('nekretnine/', NekretninaList.as_view(), name='filteri'),
    path('nekretnine/<int:pk>/', BookingDetail.as_view(), name='nekretnina_detail'),
    path('nekretnine/create/', BookingCreateView.as_view(), name='booking_create'),
    path('nekretnine/<int:pk>/delete', BookingDeleteView.as_view(), name='booking_delete'),


    path('prijava/', CustomLoginView.as_view(), name='prijava'),
    path('logout/', CustomLogoutView, name='logout'),

    path('forgot/', ForgotView.as_view(), name='forgot'),
    path('verification/', VerificationSuccessView.as_view(), name='verification'),

]
