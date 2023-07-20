import os
import django

# Replace 'your_project_name' with the name of your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# This line is necessary to configure the Django settings and initialize the app registry
django.setup()

import random
from decimal import Decimal
from django.utils.text import slugify
from booking.models import BookingPage, BookingPageGalleryImage, Agent, Image


def create_dummy_data():
    STATUS_CHOICES = ['kupovina', 'prodaja', 'iznajmljivanje']
    GRAD_CHOICES = ['banjaluka', 'okolina']
    MJESTO_CHOICES = ['mejdan', 'centar', 'borik', 'laus', 'cokori', 'slatina']
    VRSTA_CHOICES = ['kuca', 'stan', 'vikendica', 'garsonjera', 'poslovni_prostor']
    ORJENTACIJA_CHOICES = ['lijeva_obala_vrbasa', 'desna_obala_vrbasa', '10_min_od_centra',
                          '10_min_od_kastela', '5_min_od_k4', '10_min_od_kampusa',
                          '5_min_od_ukc', 'blizu_parka', 'blizu_zelenog_mosta']

    num_dummy_records = 10  # Adjust the number of dummy records as per your requirement

    for _ in range(num_dummy_records):
        naziv = f'Dummy Property {_ + 1}'
        povrsina = Decimal(random.uniform(50, 200))
        cena = Decimal(random.uniform(10000, 500000))
        opis = f'This is a dummy property description for {naziv}'
        status = random.choice(STATUS_CHOICES)
        vrsta = random.choice(VRSTA_CHOICES)
        orjentacija = random.choice(ORJENTACIJA_CHOICES)
        grad = random.choice(GRAD_CHOICES)
        mjesto = random.choice(MJESTO_CHOICES)
        dvoriste = random.choice([True, False])
        garaza = random.choice([True, False])
        bazen = random.choice([True, False])
        centralno_grijanje = random.choice([True, False])
        lift = random.choice([True, False])
        parking = random.choice([True, False])
        klima = random.choice([True, False])
        agent = Agent.objects.first()  # Replace 'Agent' with your actual Agent model class

        latitude = Decimal(random.uniform(44.706389, 44.844916))
        longitude = Decimal(random.uniform(17.035946, 17.347521))

        # Creating a slug from the property name
        slug = slugify(naziv)

        # Create a BookingPage instance with the dummy data
        booking_page = BookingPage.objects.create(
            naziv=naziv,
            povrsina=povrsina,
            cena=cena,
            opis=opis,
            status=status,
            vrsta=vrsta,
            orjentacija=orjentacija,
            grad=grad,
            mjesto=mjesto,
            dvoriste=dvoriste,
            garaza=garaza,
            bazen=bazen,
            centralno_grijanje=centralno_grijanje,
            lift=lift,
            parking=parking,
            klima=klima,
            agent = Agent.objects.get(name='agent1'),
            latitude=latitude,
            longitude=longitude,
        )

        # Add gallery images to the created BookingPage instance if needed
        # Replace 'Image' with your actual Image model class
        # Replace 'booking_page' and 'image_instance' accordingly
        if random.choice([True, False]):
            for _ in range(random.randint(1, 5)):
                image_instance = Image.objects.order_by('?').first()
                BookingPageGalleryImage.objects.create(
                    page=booking_page,
                    image=image_instance,
                    caption=f'Dummy image caption for {booking_page.naziv}',
                )
