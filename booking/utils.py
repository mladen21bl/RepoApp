import random
from django.utils.text import slugify
from .models import BookingPage

def create_dummy_data(num_instances):
    for _ in range(num_instances):
        booking_page = BookingPage()
        booking_page.naziv = f"Booking Page {random.randint(1, 100)}"
        booking_page.povrsina = random.uniform(50, 200)
        booking_page.cena = random.uniform(10000, 200000)
        booking_page.opis = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        booking_page.status = random.choice(BookingPage.STATUS_CHOICES)[0]
        booking_page.vrsta = random.choice(BookingPage.VRSTA_CHOICES)[0]
        booking_page.orjentacija = random.choice(BookingPage.ORJENTACIJA_CHOICES)[0]
        booking_page.grad = random.choice(BookingPage.GRAD_CHOICES)[0]
        booking_page.mjesto = random.choice(BookingPage.MJESTO_CHOICES)[0]
        booking_page.dvoriste = random.choice([True, False])
        booking_page.garaza = random.choice([True, False])
        booking_page.bazen = random.choice([True, False])
        booking_page.centralno_grijanje = random.choice([True, False])
        booking_page.lift = random.choice([True, False])
        booking_page.parking = random.choice([True, False])
        booking_page.klima = random.choice([True, False])
        # Assuming you have an 'Agent' instance available to assign
        booking_page.agent = agent_instance

        # Save the instance
        booking_page.save()

        # Generate a slug for the instance
        booking_page.slug = slugify(booking_page.naziv)
        booking_page.save()
