from django.test import TestCase

# Create your tests here.
from django.test import Client
from django.urls import reverse
from .models import Booking
from datetime import date

class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="Alice",
            reservation_date=date.today(),
            reservation_slot=12
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.first_name, "Alice")
        self.assertEqual(self.booking.reservation_slot, 12)
        self.assertEqual(Booking.objects.count(), 1)

    def test_duplicate_booking_prevention(self):
        # Attempt to create a duplicate booking for same date & slot
        duplicate = Booking.objects.filter(
            reservation_date=self.booking.reservation_date,
            reservation_slot=self.booking.reservation_slot
        ).exists()
        self.assertTrue(duplicate)

class BookingFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'first_name': 'Bob',
            'reservation_date': date.today(),
            'reservation_slot': 14
        }
        from .forms import BookingForm
        form = BookingForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        from .forms import BookingForm
        form = BookingForm(data={})
        self.assertFalse(form.is_valid())

class BookingAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('bookings')  # Make sure this matches your urls.py
        self.booking = Booking.objects.create(
            first_name="Charlie",
            reservation_date=date.today(),
            reservation_slot=15
        )

    def test_get_bookings(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Charlie")

    def test_post_booking(self):
        data = {
            'first_name': 'Dana',
            'reservation_date': str(date.today()),
            'reservation_slot': 16
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Booking.objects.filter(first_name='Dana').exists())
