from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from workers.models import Worker
from django.db.models import Avg

@receiver(post_save, sender=Review)
def update_worker_rating(sender, instance, **kwargs):
    worker = instance.booking.worker
    avg_rating = worker.worker_bookings.filter(
        status="completed"
    ).aggregate(Avg("review__rating"))["review__rating__avg"]

    worker.rating = avg_rating or 0
    worker.save()
