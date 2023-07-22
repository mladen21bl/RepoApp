import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

import random
from decimal import Decimal
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from booking.models import BookingPage, BookingPageGalleryImage
from wagtail.images.models import Image as WagtailImage

fake = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for BookingPage model.'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of BookingPage objects to be created.')

    def handle(self, *args, **kwargs):
        total = kwargs['total']

        STATUS_CHOICES = ['kupovina', 'prodaja', 'iznajmljivanje']
        VRSTA_CHOICES = ['kuca', 'stan', 'vikendica', 'garsonjera', 'poslovni_prostor']
        ORJENTACIJA_CHOICES = [
            'lijeva_obala_vrbasa', 'desna_obala_vrbasa', '10_min_od_centra',
            '10_min_od_kastela', '5_min_od_k4', '10_min_od_kampusa',
            '5_min_od_ukc', 'blizu_parka', 'blizu_zelenog_mosta'
        ]
        GRAD_CHOICES = ['banjaluka', 'okolina']
        MJESTO_CHOICES = ['mejdan', 'centar', 'borik', 'laus', 'cokori', 'slatina']

        for _ in range(total):
            booking_page = BookingPage.objects.create(
                naziv=fake.catch_phrase(),
                povrsina=Decimal(random.uniform(30, 200)),
                cena=Decimal(random.uniform(50000, 500000)),
                opis=fake.paragraph(),
                status=random.choice(STATUS_CHOICES),
                vrsta=random.choice(VRSTA_CHOICES),
                orjentacija=random.choice(ORJENTACIJA_CHOICES),
                grad=random.choice(GRAD_CHOICES),
                mjesto=random.choice(MJESTO_CHOICES),
                dvoriste=random.choice([True, False]),
                garaza=random.choice([True, False]),
                bazen=random.choice([True, False]),
                centralno_grijanje=random.choice([True, False]),
                lift=random.choice([True, False]),
                parking=random.choice([True, False]),
                klima=random.choice([True, False]),
                agent_id=random.randint(1, 5),  # Replace 1 and 10 with the range of Agent IDs.
                latitude=Decimal(random.uniform(44.706389, 44.844916)),
                longitude=Decimal(random.uniform(17.035946, 17.347521)),
            )

            # Generate dummy gallery images
            for _ in range(random.randint(1, 5)):  # Adjust the range as needed
                dummy_image = WagtailImage.objects.order_by('?').first()  # Get a random image
                gallery_image = BookingPageGalleryImage.objects.create(
                    page=booking_page,
                    image=dummy_image,
                    caption=fake.sentence(),
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully created BookingPage object "{booking_page.naziv}".'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} BookingPage objects.'))
