from django.db import models
from bookings.models import Booking
# Create your models here.
class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
