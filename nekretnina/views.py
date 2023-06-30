from django.shortcuts import redirect, render
from .models import Nekretnina, NekretninaPage, Agent, Korisnik, Poruke
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, FieldPanel
from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Nekretnina
from django import forms
from django.core.mail import EmailMessage
from .models import KontaktForma
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class KontaktFormaCreate(CreateView):
    model = KontaktForma
    template_name = 'nekretnina/nekretnina_detail.html'
    fields = ['upit', 'naziv_nekretnine']
    success_url = '/'

    def form_valid(self, form):
        nekretnina = get_object_or_404(Nekretnina, naziv=self.request.POST['naziv_nekretnine'])
        form.instance.ime = self.request.user.username
        form.instance.ime_agenta = nekretnina.agent
        return super().form_valid(form)


class KontaktFormaList(ListView):
    model = KontaktForma
    template_name = 'nekretnina/kontakt_forma_list.html'
    context_object_name = 'upiti'

class KontaktFormaDetail(DetailView):
    model = KontaktForma
    template_name = 'nekretnina/kontakt_forma_detail.html'
    context_object_name = 'upit'



class OdgovorView(LoginRequiredMixin, CreateView):
    model = Poruke
    template_name = 'nekretnina/odgovor.html'
    fields = ('tekst',)
    success_url = reverse_lazy('nekretnina:upit')

    def form_valid(self, form):
        form.instance.ime = self.request.user.username
        form.instance.forma_id = self.kwargs['pk']
        return super().form_valid(form)

class IndexView(TemplateView):
    template_name = 'home/home_page.html'




class NekretninaCreateView(CreateView):
    model = Nekretnina
    template_name = 'nekretnina/nekretnina_create.html'
    fields = ('__all__')
    success_url = reverse_lazy('nekretnina:nekretnina_list')

class NekretninaEditView(UpdateView):
    model = Nekretnina
    fields = ('__all__')
    template_name = 'nekretnina/nekretnina_edit.html'
    success_url = reverse_lazy('nekretnina:nekretnina_list')



class NekretninaDeleteView(DeleteView):
    model = Nekretnina
    template_name = 'nekretnina/nekretnina_delete.html'
    success_url = reverse_lazy('nekretnina:nekretnina_list')

class NekretninaList(ListView):
    model = Nekretnina
    context_object_name = 'lista'
    template_name = 'nekretnina/nekretnina_list.html'
    paginate_by = 4
    
    def get_queryset(self):
        queryset = super().get_queryset()

        naziv = self.request.GET.get('naziv')
        if naziv:
            queryset = queryset.filter(naziv__icontains=naziv)

        cena_od = self.request.GET.get('cena_od')
        cena_do = self.request.GET.get('cena_do')
        if cena_od and cena_do:
            queryset = queryset.filter(cena__range=(cena_od, cena_do))
        elif cena_od:
            queryset = queryset.filter(cena__gte=cena_od)
        elif cena_do:
            queryset = queryset.filter(cena__lte=cena_do)


        povrsina_od = self.request.GET.get('povrsina_od')
        povrsina_do = self.request.GET.get('povrsina_do')
        if povrsina_od and povrsina_do:
            queryset = queryset.filter(povrsina__range=(povrsina_od, povrsina_do))
        elif povrsina_od:
            queryset = queryset.filter(povrsina__gte=povrsina_od)
        elif povrsina_do:
            queryset = queryset.filter(povrsina__lte=povrsina_do)

        vrsta = self.request.GET.get('vrsta')
        status = self.request.GET.get('status')
        grad = self.request.GET.get('grad')
        mjesto = self.request.GET.get('mjesto')
        dvoriste = self.request.GET.get('dvoriste')
        bazen = self.request.GET.get('bazen')
        garaza = self.request.GET.get('garaza')
        centralno_grijanje = self.request.GET.get('centralno_grijanje')
        lift = self.request.GET.get('lift')
        parking = self.request.GET.get('parking')
        klima = self.request.GET.get('klima')



        if vrsta:
            queryset = queryset.filter(vrsta=vrsta)
        if status:
            queryset = queryset.filter(status=status)
        if grad:
            queryset = queryset.filter(grad=grad)
        if mjesto:
            queryset = queryset.filter(mjesto=mjesto)

        if vrsta in ['kuca', 'vikendica']:
            if dvoriste:
                queryset = queryset.filter(dvoriste=True)

            if bazen:
                queryset = queryset.filter(bazen=True)

            if garaza:
                queryset = queryset.filter(garaza=True)

        if vrsta in ['stan', 'garsonjera']:
            if centralno_grijanje:
                queryset = queryset.filter(centralno_grijanje=True)

            if lift:
                queryset = queryset.filter(lift=True)

        if vrsta in ['poslovni_prostor']:
            if parking:
                queryset = queryset.filter(parking=True)

            if klima:
                queryset = queryset.filter(klima=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vrsta_choices'] = Nekretnina.VRSTA_CHOICES
        context['status_choices'] = Nekretnina.STATUS_CHOICES
        context['grad_choices'] = Nekretnina.GRAD_CHOICES
        context['mjesto_choices'] = Nekretnina.MJESTO_CHOICES
        context['selected_vrsta'] = self.request.GET.get('vrsta', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_grad'] = self.request.GET.get('grad', '')
        context['selected_mjesto'] = self.request.GET.get('mjesto', '')
        context['selected_dvoriste'] = self.request.GET.get('dvoriste', '')
        context['selected_bazen'] = self.request.GET.get('bazen', '')
        context['selected_garaza'] = self.request.GET.get('garaza', '')
        context['selected_centralno_grijanje'] = self.request.GET.get('centralno_grijanje', '')
        context['selected_lift'] = self.request.GET.get('lift', '')
        context['selected_parking'] = self.request.GET.get('parking', '')
        context['selected_klima'] = self.request.GET.get('klima', '')

        return context

class NekretninaDetailView(DetailView):
    context_object_name = 'detail'
    model = Nekretnina
    template_name = 'nekretnina/nekretnina_detail.html'


class AgentiList(ListView):
    model = Agent
    context_object_name = 'agenti'
    template_name = 'nekretnina/agenti_list.html'



class AgentiDetailView(DetailView):
    context_object_name = 'agent'
    model = Agent
    template_name = 'nekretnina/agenti_detail.html'


class AgentCreateView(CreateView):
    model = Agent
    fields = ('ime', 'prezime', 'sifra', 'email', 'telefon')
    template_name = 'nekretnina/agent_registracija.html'
    success_url = reverse_lazy('nekretnina:indexview')

    def form_valid(self, form):
        # Stvaranje Django korisnika (User)
        username = form.cleaned_data['ime']
        password = form.cleaned_data['sifra']
        email = form.cleaned_data['email']
        user = User.objects.create_user(username=username, password=password, email=email)

        # Povezivanje Django korisnika s instancom Korisnik
        agent = form.save(commit=False)
        agent.user = user
        agent.save()

        return super().form_valid(form)


class KorisnikCreateView(CreateView):
    model = Korisnik
    fields = ('ime', 'sifra', 'email')
    template_name = 'nekretnina/korisnik_registracija.html'
    success_url = reverse_lazy('nekretnina:indexview')

    def form_valid(self, form):
        # Stvaranje Django korisnika (User)
        username = form.cleaned_data['ime']
        password = form.cleaned_data['sifra']
        email = form.cleaned_data['email']
        user = User.objects.create_user(username=username, password=password, email=email)

        # Povezivanje Django korisnika s instancom Korisnik
        korisnik = form.save(commit=False)
        korisnik.user = user
        korisnik.save()

        return super().form_valid(form)

User = get_user_model()



class CustomLoginView(LoginView):
    template_name = 'nekretnina/login.html'

    def get_success_url(self):
        return reverse_lazy('nekretnina:indexview')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        try:
            korisnik = Korisnik.objects.get(ime=username)
        except Korisnik.DoesNotExist:
            korisnik = None

        try:
            agent = Agent.objects.get(ime=username)
        except Agent.DoesNotExist:
            agent = None

        if korisnik is not None and korisnik.odobreno:
            return super().form_valid(form)
        elif agent is not None:
            if agent.sifra == password:
                return super().form_valid(form)
        elif username == 'superuser' and password == 'password':
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Pristup odbijen.')
            return redirect('nekretnina:prijava')


def CustomLogoutView(request):
    logout(request)
    return redirect('nekretnina:indexview')


class KorisnikList(ListView):
    model = Korisnik
    context_object_name = 'korisnici'
    template_name = 'nekretnina/korisnici_list.html'


class KorisnikDetailView(DetailView):
    context_object_name = 'korisnik'
    model = Korisnik
    template_name = 'nekretnina/korisnik_detail.html'
