from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, FieldPanel
from wagtail.search import index
from wagtail.images.models import Image
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User





class KontaktForma(models.Model):
    ime = models.CharField(max_length=255)
    upit = models.CharField(max_length=700)
    naziv_nekretnine = models.CharField(max_length=255)
    ime_agenta = models.CharField(max_length=255, default="007")


    def __str__(self):
        return self.ime


class Poruke(models.Model):
    ime = models.CharField(max_length=255)
    tekst = models.CharField(max_length=700)
    forma = models.ForeignKey('KontaktForma', related_name='poruke', on_delete=models.CASCADE)

    def __str__(self):
        return self.ime


class Korisnik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    ime = models.CharField(max_length=255, unique=True)
    sifra = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    odobreno = models.BooleanField(default=False)
    inbox = models.ManyToManyField(KontaktForma, blank=True)

    def __str__(self):
        return self.ime


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    ime = models.CharField(max_length=255)
    sifra = models.CharField(max_length=255)
    prezime = models.CharField(max_length=255)
    email = models.EmailField()
    telefon = models.CharField(max_length=20)
    inbox = models.ManyToManyField(KontaktForma, blank=True)

    def __str__(self):
        return self.email

    def get_admin_display_title(self):
        return f'{self.ime} {self.prezime}'



class AgentIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]



class AgentPage(Page):
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('agent'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['agent'] = self.agent
        return context


class NekretninaIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        nekretnine = Nekretnina.objects.all()
        context['nekretnine'] = nekretnine
        return context

class Nekretnina(models.Model):
    STATUS_CHOICES = [
        ('kupovina', 'Kupovina'),
        ('prodaja', 'Prodaja'),
        ('iznajmljivanje', 'Iznajmljivanje'),
    ]

    GRAD_CHOICES = [
        ('banjaluka', 'Banja Luka'),
        ('okolina', 'Okolina'),
    ]

    MJESTO_CHOICES = [
        ('mejdan', 'Mejdan'),
        ('centar', 'Centar'),
        ('borik', 'Borik'),
        ('laus', 'Laus'),
        ('cokori', 'Cokori'),
        ('slatina', 'Slatina'),
    ]

    VRSTA_CHOICES = [
        ('kuca', 'Kuća'),
        ('stan', 'Stan'),
        ('vikendica', 'Vikendica'),
        ('garsonjera', 'Garsonjera'),
        ('poslovni_prostor', 'Poslovni prostor'),
    ]

    naziv = models.CharField(max_length=255, unique=True)
    povrsina = models.DecimalField(max_digits=10, decimal_places=2)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    opis = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    vrsta = models.CharField(max_length=35, choices=VRSTA_CHOICES, default='stan')
    grad = models.CharField(max_length=15, choices=GRAD_CHOICES, default='banjaluka')
    mjesto = models.CharField(max_length=15, choices=MJESTO_CHOICES, default='centar')
    slike = models.ManyToManyField(
        Image,
        blank=True,
        related_name='nekretnina_slike'
    )
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='nekretnine')
    dvoriste = models.BooleanField(default=False)
    garaza = models.BooleanField(default=False)
    bazen = models.BooleanField(default=False)
    centralno_grijanje = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    klima = models.BooleanField(default=False)



    def get_dvoriste_display(self):
        return "Ima" if self.dvoriste else "Nema"

    def get_garaza_display(self):
        return "Ima" if self.garaza else "Nema"

    def get_bazen_display(self):
        return "Ima" if self.bazen else "Nema"

    def get_centralno_grijanje_display(self):
        return "Ima" if self.centralno_grijanje else "Nema"

    def get_lift_display(self):
        return "Ima" if self.lift else "Nema"

    def get_parking_display(self):
        return "Ima" if self.parking else "Nema"

    def get_klima_display(self):
        return "Ima" if self.klima else "Nema"

    def save(self, *args, **kwargs):
        if self.vrsta != 'kuca':
            self.dvoriste = False
            self.garaza = False
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('nekretnina_page', args=[str(self.id)])

    def __str__(self):
        return self.naziv



class NekretninaPage(Page):
    nekretnina = models.ForeignKey(Nekretnina, null=True, blank=True, on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('nekretnina'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['nekretnina'] = self.nekretnina
        return context
