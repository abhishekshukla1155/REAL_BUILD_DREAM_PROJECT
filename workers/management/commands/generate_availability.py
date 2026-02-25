from django.core.management.base import BaseCommand
from workers.models import Worker, WorkerAvailability
from datetime import time

class Command(BaseCommand):
    help = "Generate availability for all workers"

    def handle(self, *args, **kwargs):

        workers = Worker.objects.all()

        for worker in workers:
            for day in range(6):  # Monday-Saturday
                WorkerAvailability.objects.get_or_create(
                    worker=worker,
                    day_of_week=day,
                    start_time=time(9, 0),
                    end_time=time(18, 0),
                )

        self.stdout.write(self.style.SUCCESS("Availability created!"))
