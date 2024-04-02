import random

from django.core.management.base import BaseCommand

from users.models import User
from events import models as event_models


def random_event(all_events):
    return random.choice(all_events)


def random_rating():
    return random.randint(1, 5)


class Command(BaseCommand):
    help = "This command creates events"

    def handle(self, *args, **options):
        all_users = User.objects.all()
        all_events = event_models.Event.objects.all()
        event_count = event_models.Event.objects.count()
        for user in all_users:
            for i in range(3):
                event = random_event(all_events)
                event_id = event.pk
                event_d, created = event_models.EventUserRating.objects.get_or_create(event_id=event_id, user_id=user.pk)
                if created:
                    event_d.rating = random_rating()
                    event_d.save()

        self.stdout.write(self.style.SUCCESS(f"dependencies created!"))
