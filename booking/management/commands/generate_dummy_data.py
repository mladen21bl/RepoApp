import os
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from booking.models import BookingPage, Agent, BookingPage, BookingIndexPage
import re

class Command(BaseCommand):
    help = 'Generates dummy data for BookingPage model.'

    STATUS_CHOICES = ['kupovina', 'prodaja', 'iznajmljivanje']
    VRSTA_CHOICES = ['kuca', 'stan', 'vikendica', 'garsonjera', 'poslovni_prostor']
    ORJENTACIJA_CHOICES = [
        'Lijeva obala Vrbasa', 'Desna obala Vrbasa', '5 min od centra', '10 min od Kastela',
        '5 min od K4', '10 min od kampusa', '5 min od UKC-a', 'Blizu parka', 'Blizu zelenog Mosta'
    ]
    GRAD_CHOICES = ['banjaluka', 'okolina']
    MJESTO_CHOICES = ['mejdan', 'centar', 'borik', 'laus', 'cokori', 'slatina']
    MAX_LATITUDE = 44.844916
    MIN_LATITUDE = 44.706389
    MAX_LONGITUDE = 17.347521
    MIN_LONGITUDE = 17.035946

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of dummy objects to be created.')

    def generate_random_coords(self):
        latitude = Decimal(random.uniform(self.MIN_LATITUDE, self.MAX_LATITUDE))
        longitude = Decimal(random.uniform(self.MIN_LONGITUDE, self.MAX_LONGITUDE))
        return latitude, longitude

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        agent_name = 'agent1'

        try:
            agent = Agent.objects.get(username=agent_name)
        except Agent.DoesNotExist:
            return

        parent_page = BookingIndexPage.objects.filter(title='listing').first()
        if not parent_page:

            return

        for _ in range(total):
            latitude, longitude = self.generate_random_coords()
            title = fake.company()
            slug = title.lower().replace(' ', '-')
            path = f'/{slug}/'
            depth = 1

            povrsina = Decimal(random.uniform(30, 200)).quantize(Decimal('0.01'))
            cena = Decimal(random.uniform(50000, 1000000)).quantize(Decimal('0.01'))
            image_path = os.path.join('media', 'original_images', 'berza.jpg')

            booking_page = BookingPage(
                title = fake.company(),
                slug = re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '-'),
                agent_id=agent.pk,
                naziv=title,
                povrsina=povrsina,
                cena=cena,
                opis=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
                status=random.choice(self.STATUS_CHOICES),
                vrsta=random.choice(self.VRSTA_CHOICES),
                orjentacija=random.choice(self.ORJENTACIJA_CHOICES),
                grad=random.choice(self.GRAD_CHOICES),
                mjesto=random.choice(self.MJESTO_CHOICES),
                dvoriste=random.choice([True, False]),
                garaza=random.choice([True, False]),
                bazen=random.choice([True, False]),
                centralno_grijanje=random.choice([True, False]),
                lift=random.choice([True, False]),
                parking=random.choice([True, False]),
                klima=random.choice([True, False]),
                latitude = Decimal(random.uniform(self.MIN_LATITUDE, self.MAX_LATITUDE)).quantize(Decimal('0.000001')),
                longitude = Decimal(random.uniform(self.MIN_LONGITUDE, self.MAX_LONGITUDE)).quantize(Decimal('0.000001')),
                slike=image_path,
            )

            booking_page = parent_page.add_child(instance=booking_page)
            booking_page.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} BookingPage objects.'))
