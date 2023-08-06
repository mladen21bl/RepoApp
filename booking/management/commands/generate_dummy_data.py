import os
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from booking.models import BookingPage, Agent, BookingIndexPage, Karakteristika, Tip, BookingPageGalleryImage
import re
from django.core.files import File
from wagtail.images.models import Image
from booking.forms import BookingPageForm

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
    MAX_LATITUDE = 44.806040
    MIN_LATITUDE = 44.758424
    MAX_LONGITUDE = 17.232666
    MIN_LONGITUDE = 17.156604


    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of dummy objects to be created.')

    def generate_random_coords(self):
        latitude = Decimal(random.uniform(self.MIN_LATITUDE, self.MAX_LATITUDE))
        longitude = Decimal(random.uniform(self.MIN_LONGITUDE, self.MAX_LONGITUDE))
        return latitude, longitude

    def save_image_to_media_folder(self, image_path):
        new_file_name = f"dummy_{random.randint(1000, 9999)}_{os.path.basename(image_path)}"
        new_image_path = os.path.join("media", "original_images", new_file_name)

        with open(image_path, 'rb') as src_file, open(new_image_path, 'wb') as dst_file:
            dst_file.write(src_file.read())

        return new_image_path


    def create_wagtail_image(self, image_path, booking_page):
        with open(image_path, 'rb') as f:
            wagtail_image = Image(title=os.path.basename(image_path), file=File(f))
            wagtail_image.save()

        gallery_image = BookingPageGalleryImage(image=wagtail_image, page=booking_page)
        gallery_image.save()

        return gallery_image

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']

        karakteristike = Karakteristika.objects.all()
        karakteristika = random.choice(karakteristike)

        broj_karakteristika = random.randint(1, 5)
        odabrane_karakteristike = random.sample(list(karakteristike), broj_karakteristika)

        agents = Agent.objects.all()
        if not agents.exists():
            return
        agent = random.choice(agents)


        parent_page = BookingIndexPage.objects.filter(title='listing').first()
        if not parent_page:
            return


        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_folder = os.path.join(base_dir, 'media', 'original_images')

        if not os.path.exists(image_folder):
            raise FileNotFoundError(f"The '{image_folder}' directory does not exist. Please create it and add images.")

        image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

        for _ in range(total):
            latitude, longitude = self.generate_random_coords()
            title = fake.company()
            naziv = title,
            slug = title.lower().replace(' ', '-')
            path = f'/{slug}/'
            depth = 1

            povrsina = Decimal(random.uniform(30, 200)).quantize(Decimal('0.01'))
            cena = Decimal(random.uniform(50000, 1000000)).quantize(Decimal('0.01'))

            image_file = random.choice(image_files)
            image_path = os.path.join(image_folder, image_file)
            new_image_path = self.save_image_to_media_folder(image_path)

            booking_page = BookingPage(
                title=fake.company(),
                slug=re.sub(r'[^\w\s-]', '', title).strip().lower().replace(' ', '-'),
                agent=agent,
                povrsina=povrsina,
                cena=cena,
                naziv=title,
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
                latitude=Decimal(random.uniform(self.MIN_LATITUDE, self.MAX_LATITUDE)).quantize(Decimal('0.000001')),
                longitude=Decimal(random.uniform(self.MIN_LONGITUDE, self.MAX_LONGITUDE)).quantize(Decimal('0.000001')),
            )

            booking_page = parent_page.add_child(instance=booking_page)
            booking_page.save()

            gallery_image = self.create_wagtail_image(new_image_path, booking_page)
            booking_page.gallery_images.add(gallery_image)


            booking_page.karakteristika.set(odabrane_karakteristike)
            booking_page.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} BookingPage objects.'))
