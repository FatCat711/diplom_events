from django.db import models
from django.urls import reverse

from users.models import User
from core import models as core_models


class Event(core_models.TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    online = models.BooleanField(default=True)
    city = models.CharField(max_length=60, null=True)
    street = models.CharField(blank=True, null=True, max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", related_name="events", blank=True)
    participants = models.ManyToManyField(
        User, related_name="events", blank=True)
    preview = models.ImageField(upload_to="event_photo", blank=True, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def review_sum(self):
        reviews = EventUserRating.objects.filter(event_id=self.pk)
        summ = 0
        for r in reviews:
            summ += r.rating
        count = 1 if reviews.count() == 0 else reviews.count()
        return round(summ/count, 2)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.title}"


class Tag(core_models.TimeStampedModel):
    title = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.title}"


class EventUserRating(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(default=1)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"user: {self.user.pk, self.user.username} event: {self.event.pk}"
