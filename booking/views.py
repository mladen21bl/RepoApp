from django.shortcuts import render, get_object_or_404, redirect
from .models import Agent, Korisnik, KontaktForma, Poruke, BookingPage, BookingIndexPage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.forms import Textarea
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
import smtplib
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.edit import FormView
from .forms import BookingPageForm

class BookingCreateView(CreateView):
    model = BookingPage
    template_name = 'booking/booking_create.html'
    form_class = BookingPageForm
    success_url = '/'

    def form_valid(self, form):
        return super().form_valid(form)

class BookingDetail(DetailView):
    context_object_name = 'detail'
    model = BookingPage
    template_name = 'booking/booking_detail.html'


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


class KorisnikCreateView(CreateView):
    model = Korisnik
    fields = ('username', 'sifra', 'email')
    template_name = 'booking/korisnik_registracija.html'
    success_url = reverse_lazy('booking:indexview')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['sifra']
        email = form.cleaned_data['email']
        user = User.objects.create_user(username=username, password=password, email=email)


        korisnik = form.save(commit=False)
        korisnik.user = user
        korisnik.save()

        return super().form_valid(form)





class CustomLoginView(LoginView):
    template_name = 'booking/login.html'

    def get_success_url(self):
        return reverse_lazy('booking:indexview')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        try:
            korisnik = Korisnik.objects.get(username=username)
        except Korisnik.DoesNotExist:
            korisnik = None

        try:
            agent = Agent.objects.get(username=username)
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
            return redirect('booking:prijava')


def CustomLogoutView(request):
    logout(request)
    return redirect('booking:indexview')


class CustomLoginView(LoginView):
    template_name = 'booking/login.html'

    def get_success_url(self):
        return reverse_lazy('booking:indexview')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        try:
            korisnik = Korisnik.objects.get(username=username)
        except Korisnik.DoesNotExist:
            korisnik = None

        try:
            agent = Agent.objects.get(username=username)
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
            return redirect('booking:prijava')



class ForgotView(TemplateView):
    template_name = 'booking/forgot_password.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        email_subject = "Verifikacija emaila"
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = [email]

        html_message = render_to_string('booking/email.html', {'message': 'Pozdrav'})
        plain_message = strip_tags(html_message)

        try:
            email = EmailMultiAlternatives(email_subject, plain_message, email_from, email_to)
            email.attach_alternative(html_message, "text/html")
            email.send()
        except Exception as e:
            print(f"Error sending email: {str(e)}")

        return redirect('booking:verification')

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



class NekretninaList(ListView):
    model = BookingPage
    context_object_name = 'lista'
    template_name = 'booking/nekretnina_list.html'
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
        context['vrsta_choices'] = BookingPage.VRSTA_CHOICES
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

        return context
