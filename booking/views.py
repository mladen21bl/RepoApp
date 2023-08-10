from django.shortcuts import render, get_object_or_404, redirect
from .models import Agent, Korisnik, KontaktForma, Poruke, BookingPage, BookingIndexPage, BookingPageGalleryImage, Karakteristika, Tip
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, View, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
import smtplib
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.edit import FormView
from .forms import BookingPageForm, ForgotPasswordForm
from django.forms import Textarea
from wagtail.models import Page, Orderable
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from wagtail.images.models import Image
from django.db import IntegrityError
from django.contrib import messages
from wagtail.images.models import Image as WagtailImage
from django.core.paginator import Paginator, Page
from django.http import JsonResponse



class BookingMapList(ListView):
    model = BookingPage
    context_object_name = 'nekretnine'
    template_name = 'booking/mapa.html'

    def get_queryset(self):
        return BookingPage.objects.all()

class SentView(TemplateView):
    template_name = 'booking/sent.html'

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

class TipCreateView(CreateView):
    model = Tip
    template_name = 'booking/tip_create.html'
    fields = ['name']
    success_url = reverse_lazy('booking:filteri')

class KarakteristikaCreateView(CreateView):
    model = Karakteristika
    template_name = 'booking/karakteristika_create.html'
    fields = ['name', 'tip']
    success_url = reverse_lazy('booking:filteri')


class BookingCreateView(CreateView):
    model = BookingPage
    template_name = 'booking/booking_create.html'
    form_class = BookingPageForm
    success_url = '/'

    def form_valid(self, form):
        parent_page = BookingIndexPage.objects.first()
        karakteristikas_list = Karakteristika.objects.filter(id__in=form.cleaned_data.get('karakteristika'))
        tips_list = Tip.objects.filter(id__in=form.cleaned_data.get('tip'))
        booking_page = form.save(commit=False)
        booking_page.title = form.cleaned_data['naziv']
        booking_page.slug = booking_page.title.lower().replace(' ', '-')

        if parent_page.specific_class == BookingIndexPage:
            booking_page.path = parent_page.path + booking_page.slug + '/'
            booking_page.depth = parent_page.depth + 1
        else:
            booking_page.path = parent_page.path + booking_page.slug + '/'
            booking_page.depth = parent_page.depth + 1

        parent_page.add_child(instance=booking_page)
        booking_page.tip.set(tips_list)
        booking_page.karakteristika.set(karakteristikas_list)

        images = self.request.FILES.getlist('slike')
        if images:
            for image in images:
                wagtail_image = WagtailImage(title=image.name)
                wagtail_image.file.save(image.name, image)
                wagtail_image.save()

                gallery_image = BookingPageGalleryImage(image=wagtail_image)
                booking_page.gallery_images.add(gallery_image)

        booking_page.save_revision().publish()

        return HttpResponseRedirect(reverse('booking:filteri'))


class BookingEditView(UpdateView):
    model = BookingPage
    form_class = BookingPageForm
    template_name = 'booking/booking_edit.html'
    success_url = reverse_lazy('booking:filteri')

    def form_valid(self, form):
        booking_page = form.save(commit=False)
        booking_page.slug = booking_page.title.lower().replace(' ', '-')
        booking_page.save()

        existing_images = booking_page.gallery_images.all()

        images = self.request.FILES.getlist('slike')
        if images:
            for image in images:
                wagtail_image = WagtailImage(title=image.name)
                wagtail_image.file.save(image.name, image)
                wagtail_image.save()

                gallery_image = BookingPageGalleryImage(image=wagtail_image)
                booking_page.gallery_images.add(gallery_image)

        booking_page.save_revision().publish()

        return super().form_valid(form)


class BookingDetail(DetailView):
    context_object_name = 'detail'
    model = BookingPage
    template_name = 'booking/booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detail = self.object
        karakteristikas = detail.karakteristika.all()

        grouped_karakteristikas = {}
        for karakteristika in karakteristikas:
            if karakteristika.tip in grouped_karakteristikas:
                grouped_karakteristikas[karakteristika.tip].append(karakteristika.name)
            else:
                grouped_karakteristikas[karakteristika.tip] = [karakteristika.name]

        context['grouped_karakteristikas'] = grouped_karakteristikas
        return context

class BookingDeleteView(DeleteView):
    model = BookingPage
    template_name = 'booking/booking_delete.html'
    success_url = reverse_lazy('booking:filteri')

class KontaktFormaCreate(CreateView):
    model = KontaktForma
    template_name = 'booking/booking_page.html'
    fields = ['upit', 'naziv_nekretnine']
    success_url = '/'

    def form_valid(self, form):
        nekretnina = get_object_or_404(BookingPage, naziv=self.request.POST['naziv_nekretnine'])
        form.instance.ime = self.request.user.username
        form.instance.ime_agenta = nekretnina.agent
        return super().form_valid(form)


class KontaktFormaList(ListView):
    model = KontaktForma
    template_name = 'booking/kontakt_forma_list.html'
    context_object_name = 'upiti'

class KontaktFormaDetail(DetailView):
    model = KontaktForma
    template_name = 'booking/kontakt_forma_detail.html'
    context_object_name = 'upit'



class OdgovorView(LoginRequiredMixin, CreateView):
    model = Poruke
    template_name = 'booking/odgovor.html'
    fields = ('tekst',)
    success_url = reverse_lazy('booking:upit')

    def form_valid(self, form):
        form.instance.ime = self.request.user.username
        form.instance.forma_id = self.kwargs['pk']
        return super().form_valid(form)


User = get_user_model()


class AgentCreateView(CreateView):
    model = Agent
    fields = ('username', 'sifra', 'email', 'telefon')
    template_name = 'booking/agent_registracija.html'
    success_url = reverse_lazy('booking:indexview')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['sifra']
        email = form.cleaned_data['email']
        user = User.objects.create_user(username=username, password=password, email=email)

        agent = form.save(commit=False)
        agent.user = user
        agent.save()

        return super().form_valid(form)

class AgentDeleteView(DeleteView):
    model = Agent
    template_name = 'booking/agent_delete.html'
    success_url = reverse_lazy('booking:agenti_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        user = self.object.user
        email = user.email
        self.object.delete()
        user.delete()

        users_with_same_email = User.objects.filter(email=email)
        if users_with_same_email.count() == 1:
            users_with_same_email.update(email='')

        logout(request)

        return HttpResponseRedirect(self.get_success_url())

class KorisnikCreateView(CreateView):
    model = Korisnik
    fields = ('username', 'sifra', 'email')
    template_name = 'booking/korisnik_registracija.html'
    success_url = reverse_lazy('booking:indexview')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['sifra']
        email = form.cleaned_data['email']

        try:
            user = User.objects.create_user(username=username, password=password, email=email)

            korisnik = form.save(commit=False)
            korisnik.user = user
            korisnik.save()

            return super().form_valid(form)
        except IntegrityError as e:
            error_message = str(e)
            if 'username' in error_message:
                messages.error(self.request, 'Korisnik sa tim korisničkim imenom već postoji.')
            elif 'email' in error_message:
                messages.error(self.request, 'Korisnik sa tim emailom već postoji.')
            else:
                messages.error(self.request, 'Greška prilikom registracije.')
            return self.form_invalid(form)


class KorisnikDeleteView(DeleteView):
    model = Korisnik
    template_name = 'booking/korisnik_delete.html'
    success_url = reverse_lazy('booking:korisnik_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        user = self.object.user
        email = user.email
        self.object.delete()
        user.delete()

        users_with_same_email = User.objects.filter(email=email)
        if users_with_same_email.count() == 1:
            users_with_same_email.update(email='')

        logout(request)

        return HttpResponseRedirect(self.get_success_url())

class CustomLoginView(LoginView):
    template_name = 'booking/login.html'
    success_url = reverse_lazy('booking:indexview')

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy('booking:indexview')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(self.request, user)
                return super().form_valid(form)

            try:
                korisnik = Korisnik.objects.get(user=user)

                if korisnik.odobreno:
                    login(self.request, user)
                    return super().form_valid(form)
                else:
                    messages.error(self.request, 'Pristup odbijen. Vas nalog jos nije odobren.')
                    return redirect('booking:prijava')
            except Korisnik.DoesNotExist:
                try:
                    agent = Agent.objects.get(user=user)
                    login(self.request, user)
                    return super().form_valid(form)
                except Agent.DoesNotExist:
                    messages.error(self.request, 'Pristup odbijen. Pogresni podaci.')
                    return redirect('booking:prijava')
        else:
            messages.error(self.request, 'Pogresni podaci.')
            return redirect('booking:prijava')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                current_site = get_current_site(request)
                mail_subject = 'Resetovanje šifre'
                message = render_to_string('booking/reset_password_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })

                msg = MIMEMultipart()
                msg['From'] = settings.DEFAULT_FROM_EMAIL
                msg['To'] = email
                msg['Subject'] = mail_subject
                msg.attach(MIMEText(message, 'html'))

                try:
                    smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                    smtp_server.ehlo()
                    smtp_server.starttls()
                    smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    smtp_server.send_message(msg)
                    smtp_server.quit()
                    messages.success(request, 'Link za resetovanje šifre je poslat na vašu email adresu.')
                    return redirect('booking:sent')
                except Exception as e:
                    messages.error(request, f'Greška prilikom slanja emaila: {e}')
            else:
                messages.error(request, 'Korisnik sa unetom email adresom ne postoji.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'booking/forgot_password.html', {'form': form})


class ResetPasswordView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'booking/reset_password.html')
        else:
            messages.error(request, 'Link za resetovanje šifre je nevažeći.')
            return redirect('booking:indexview')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Vaša šifra je uspešno resetovana. Možete se prijaviti sa novom šifrom.')
                return redirect('booking:prijava')
            else:
                messages.error(request, 'Unete šifre se ne podudaraju.')
        else:
            messages.error(request, 'Link za resetovanje šifre je nevažeći.')

        return render(request, 'booking/reset_password.html')

reset_password = method_decorator(csrf_exempt)(ResetPasswordView.as_view())

def CustomLogoutView(request):
    logout(request)
    return redirect('booking:indexview')



class VerificationSuccessView(TemplateView):
    template_name = 'booking/verification_success.html'

class KorisnikList(ListView):
    model = Korisnik
    context_object_name = 'korisnici'
    template_name = 'booking/korisnici_list.html'


class KorisnikDetailView(DetailView):
    context_object_name = 'korisnik'
    model = Korisnik
    template_name = 'booking/korisnik_detail.html'


class IndexView(TemplateView):
    template_name = 'home/home_page.html'


class AgentiList(ListView):
    model = Agent
    context_object_name = 'agenti'
    template_name = 'booking/agenti_list.html'



class AgentiDetailView(DetailView):
    context_object_name = 'agent'
    model = Agent
    template_name = 'booking/agenti_detail.html'





class NekretninaList(ListView):
    model = BookingPage
    context_object_name = 'lista'
    template_name = 'booking/nekretnina_list.html'


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
        orjentacija = self.request.GET.get('orjentacija')
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
        context['vrsta_choices'] = BookingPage.VRSTA_CHOICES
        context['orjentacija_choices'] = BookingPage.ORJENTACIJA_CHOICES
        context['status_choices'] = BookingPage.STATUS_CHOICES
        context['grad_choices'] = BookingPage.GRAD_CHOICES
        context['mjesto_choices'] = BookingPage.MJESTO_CHOICES
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

        paginator = Paginator(context['lista'], 10)
        page_number = self.request.GET.get('page')
        paginated_lista = paginator.get_page(page_number)
        context['paginated_lista'] = paginated_lista
        return context
