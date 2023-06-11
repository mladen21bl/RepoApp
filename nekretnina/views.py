from django.shortcuts import redirect, render
from .models import Nekretnina, NekretninaPage, Agent, Korisnik
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
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect



def kontakt_forma(request):
    if request.method == 'POST':
        ime = request.POST.get('ime')
        poruka = request.POST.get('poruka')
        nekretnina_pk = request.POST.get('nekretnina_pk')
        naziv_nekretnine = request.POST.get('naziv_nekretnine')

        nekretnina = Nekretnina.objects.get(pk=nekretnina_pk)

        kontakt_forma = KontaktForma(ime=ime, poruka=poruka, naziv_nekretnine=naziv_nekretnine)
        kontakt_forma.save()

        agent = nekretnina.agent
        agent.inbox.add(kontakt_forma)

        return redirect('nekretnina:nekretnina_detail', pk=nekretnina_pk)

    return redirect('nekretnina:nekretnina_list')


class IndexView(TemplateView):
    template_name = 'home/home_page.html'


class NekretninaList(ListView):
    model = Nekretnina
    context_object_name = 'lista'
    template_name = 'nekretnina/nekretnina_list.html'

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



class KorisnikCreateView(CreateView):
    model = Korisnik
    fields = ('ime', 'sifra', 'email')
    template_name = 'nekretnina/korisnik_registracija.html'
    success_url = reverse_lazy('nekretnina:indexview')

    def form_valid(self, form):
        form.instance.odobreno = False
        return super().form_valid(form)


class KorisnikList(ListView):
    model = Korisnik
    context_object_name = 'korisnici'
    template_name = 'nekretnina/korisnici_list.html'


class KorisnikDetailView(DetailView):
    context_object_name = 'korisnik'
    model = Korisnik
    template_name = 'nekretnina/korisnik_detail.html'
