from django.core.management.base import BaseCommand

from users.models import User
from events import models as event_models


class Command(BaseCommand):
    help = "This command creates events"

    def handle(self, *args, **options):
        events = event_models.Event.objects.all()
        admin = User.objects.get(pk=1)
        for event in events:
            if event.host is None:
                event.host = admin
                event.save()

        self.stdout.write(self.style.SUCCESS("Complete!"))
