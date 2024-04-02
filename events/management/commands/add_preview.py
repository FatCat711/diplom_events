import random

from django.core.management.base import BaseCommand

from events import models as event_models


class Command(BaseCommand):
    help = "This command creates events"

    def handle(self, *args, **options):
        for event in event_models.Event.objects.all():
            event.preview = f"event_photo/{random.randint(1, 10)}.jpg"
            event.save()
        self.stdout.write(self.style.SUCCESS("previews added"))
