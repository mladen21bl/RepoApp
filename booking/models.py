from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from django.contrib.auth.models import User
from wagtail.images.models import Image
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill




class KontaktForma(models.Model):
    ime = models.CharField(max_length=255)
    upit = models.CharField(max_length=700)
    naziv_nekretnine = models.CharField(max_length=255)
    ime_agenta = models.CharField(max_length=255)


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
    username = models.CharField(max_length=255)
    sifra = models.CharField(max_length=255)
    email = models.EmailField()
    odobreno = models.BooleanField(default=False)
    inbox = models.ManyToManyField(KontaktForma, blank=True)
    is_agent = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    username = models.CharField(max_length=255, unique=True)
    sifra = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=20)
    inbox = models.ManyToManyField(KontaktForma, blank=True)
    odobreno = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=True)


    def __str__(self):
        return self.username

    def get_admin_display_title(self):
        return f'{self.username}'




class AgentPage(Page):
    username = models.CharField(max_length=255, unique=True)
    sifra = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=20)

    def __str__(self):
        return self.username

    def get_admin_display_title(self):
        return f'{self.username}'

    content_panels = Page.content_panels + [
        FieldPanel('username'),
        FieldPanel('sifra'),
        FieldPanel('email'),
        FieldPanel('telefon'),

    ]

class BookingIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        queryset = self.get_queryset(request)

        context['vrsta_choices'] = BookingPage.VRSTA_CHOICES
        context['status_choices'] = BookingPage.STATUS_CHOICES
        context['grad_choices'] = BookingPage.GRAD_CHOICES
        context['mjesto_choices'] = BookingPage.MJESTO_CHOICES
        context['selected_vrsta'] = request.GET.get('vrsta', '')
        context['selected_status'] = request.GET.get('status', '')
        context['selected_grad'] = request.GET.get('grad', '')
        context['selected_mjesto'] = request.GET.get('mjesto', '')
        context['selected_dvoriste'] = request.GET.get('dvoriste', '')
        context['selected_bazen'] = request.GET.get('bazen', '')
        context['selected_garaza'] = request.GET.get('garaza', '')
        context['selected_centralno_grijanje'] = request.GET.get('centralno_grijanje', '')
        context['selected_lift'] = request.GET.get('lift', '')
        context['selected_parking'] = request.GET.get('parking', '')
        context['selected_klima'] = request.GET.get('klima', '')

        context['lista'] = queryset

        return context

    def get_queryset(self, request):
        queryset = BookingPage.objects.live()

        naziv = request.GET.get('naziv')
        if naziv:
            queryset = queryset.filter(naziv__icontains=naziv)

        cena_od = request.GET.get('cena_od')
        cena_do = request.GET.get('cena_do')
        if cena_od and cena_do:
            queryset = queryset.filter(cena__range=(cena_od, cena_do))
        elif cena_od:
            queryset = queryset.filter(cena__gte=cena_od)
        elif cena_do:
            queryset = queryset.filter(cena__lte=cena_do)

        povrsina_od = request.GET.get('povrsina_od')
        povrsina_do = request.GET.get('povrsina_do')
        if povrsina_od and povrsina_do:
            queryset = queryset.filter(povrsina__range=(povrsina_od, povrsina_do))
        elif povrsina_od:
            queryset = queryset.filter(povrsina__gte=povrsina_od)
        elif povrsina_do:
            queryset = queryset.filter(povrsina__lte=povrsina_do)

        vrsta = request.GET.get('vrsta')
        status = request.GET.get('status')
        grad = request.GET.get('grad')
        mjesto = request.GET.get('mjesto')
        dvoriste = request.GET.get('dvoriste')
        bazen = request.GET.get('bazen')
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




class BookingPage(Page):
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

    ORJENTACIJA_CHOICES = [
        ('Lijeva obala Vrbasa', 'lijeva_obala_vrbasa'),
        ('Desna obala Vrbasa', 'desna_obala_vrbasa'),
        ('5 min od centra', '10_min_od_centra'),
        ('10 min od Kastela', '10_min_od_kastela'),
        ('5 min od K4', '5_min_od_k4'),
        ('10 min od kampusa', '10_min_od_kampusa'),
        ('5 min od UKC-a', '5_min_od_ukc'),
        ('Blizu parka', 'blizu_parka'),
        ('Blizu zelenog Mosta', 'blizu_zelenog_mosta'),

    ]

    naziv = models.CharField(max_length=255, unique=True)
    povrsina = models.DecimalField(max_digits=10, decimal_places=2)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    opis = RichTextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    vrsta = models.CharField(max_length=35, choices=VRSTA_CHOICES, default='stan')
    orjentacija = models.CharField(max_length=35, choices=ORJENTACIJA_CHOICES, default='desna_obala_vrbasa')
    grad = models.CharField(max_length=15, choices=GRAD_CHOICES, default='banjaluka')
    mjesto = models.CharField(max_length=15, choices=MJESTO_CHOICES, default='centar')
    dvoriste = models.BooleanField(default=False)
    garaza = models.BooleanField(default=False)
    bazen = models.BooleanField(default=False)
    centralno_grijanje = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    klima = models.BooleanField(default=False)
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='nekretnine')
    slike = models.ManyToManyField(Image)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image = models.ImageField(upload_to='original_images/', default='stan.jpg')



    search_fields = Page.search_fields + [
        index.SearchField('naziv'),
        index.SearchField('povrsina'),
        index.SearchField('cena'),
        index.SearchField('opis'),
        index.SearchField('status'),
        index.SearchField('vrsta'),
        index.SearchField('grad'),
        index.SearchField('mjesto'),
        index.SearchField('dvoriste'),
        index.SearchField('garaza'),
        index.SearchField('bazen'),
        index.SearchField('lift'),
        index.SearchField('centralno_grijanje'),
        index.SearchField('parking'),
        index.SearchField('klima'),
        index.SearchField('agent'),
        index.SearchField('slike'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('naziv'),
        FieldPanel('povrsina'),
        FieldPanel('agent'),
        FieldPanel('cena'),
        FieldPanel('opis'),
        FieldPanel('status'),
        FieldPanel('vrsta'),
        FieldPanel('orjentacija'),
        FieldPanel('grad'),
        FieldPanel('mjesto'),
        FieldPanel('dvoriste'),
        FieldPanel('garaza'),
        FieldPanel('bazen'),
        FieldPanel('centralno_grijanje'),
        FieldPanel('lift'),
        FieldPanel('parking'),
        FieldPanel('klima'),
        FieldPanel('slike'),
        FieldPanel('latitude'),
        FieldPanel('longitude'),
        InlinePanel('gallery_images', label="Gallery images"),

    ]

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

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
        return reverse('booking:nekretnina_detail', args=[str(self.id)])

    def __str__(self):
        return self.naziv



class BookingPageGalleryImage(Orderable):
    page = ParentalKey(BookingPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
    'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]



class AgentIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
