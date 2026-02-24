import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from workers.models import Worker

User = get_user_model()


class Command(BaseCommand):
    help = "Import workers from CSV"

    def handle(self, *args, **kwargs):

        file_path = "core/worker_data/build_workers_dataset .csv"

        workers_to_create = []
        users_to_create = []
        seen_usernames = set()

        # =========================
        # CREATE USERS
        # =========================
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

                worker_id = row.get("worker_id")

                # Skip blank IDs
                if not worker_id:
                    continue

                username = f"worker_{worker_id}"

                # Skip duplicate usernames inside CSV
                if username in seen_usernames:
                    continue

                seen_usernames.add(username)

                user = User(
                    username=username,
                    phone=row.get("worker_number"),
                    user_type="worker"
                )
                user.set_password("worker123")
                users_to_create.append(user)

        # Bulk create users
        User.objects.bulk_create(users_to_create)

        # =========================
        # CREATE WORKER PROFILES
        # =========================
        created_users = User.objects.filter(user_type="worker")
        user_map = {u.username: u for u in created_users}

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

                worker_id = row.get("worker_id")
                if not worker_id:
                    continue

                username = f"worker_{worker_id}"

                if username not in user_map:
                    continue

                worker = Worker(
                    user=user_map[username],
                    category=row["worker_profession"].lower(),
                    experience=int(float(row["worker_experience"])),
                    rating=Decimal(row["worker_rating"]),
                    latitude=float(row["Latitude"]),
                    longitude=float(row["Longitude"]),
                    price_per_hour=Decimal("500.00"),
                )

                workers_to_create.append(worker)

        Worker.objects.bulk_create(workers_to_create)

        self.stdout.write(
            self.style.SUCCESS("✅ Successfully imported workers!")
        )
