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
