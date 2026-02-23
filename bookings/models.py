from django.db import models
from django.conf import settings
from workers.models import Worker
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_bookings',
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name='worker_bookings'
    )
    service_address = models.TextField()

    booking_date = models.DateField(null=True, blank=True)
    booking_time = models.TimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.username} - {self.worker.user.username}'