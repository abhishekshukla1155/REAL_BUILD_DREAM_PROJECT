from django.db import models
from django.conf import settings

class Worker(models.Model):
    CATEGORY_CHOICES = (
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('carpenter', 'Carpenter'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    experience = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(default=0)
    is_available = models.BooleanField(default=True)
    city = models.CharField(max_length=100, default='Kanpur')

    def __str__(self):
        return f"{self.user.username} - {self.category}"

class WorkerAvailability(models.Model):
    DAYS_OF_WEEK = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )

    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name="availability_slots"
    )

    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.worker.user.username} - {self.get_day_of_week_display()}"


