from django.db import models
from django.urls import reverse

from users.models import User
from core import models as core_models

from events.partials.mail import send_mail


class Event(core_models.TimeStampedModel):
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    title = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(blank=True, null=True, verbose_name="описание")
    online = models.BooleanField(default=True, verbose_name="онлайн")
    city = models.CharField(max_length=60, null=True, verbose_name="город")
    street = models.CharField(blank=True, null=True, max_length=100, verbose_name="улица")
    time_start = models.DateTimeField(verbose_name="время начала")
    time_end = models.DateTimeField(blank=True, null=True, verbose_name="время конца")
    tags = models.ManyToManyField("Tag", related_name="events", blank=True, verbose_name="теги")
    participants = models.ManyToManyField(
        User, related_name="events", blank=True, verbose_name="участники")
    preview = models.ImageField(upload_to="event_photo", blank=True, null=True, verbose_name="превью")
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="организатор")

    def review_sum(self):
        reviews = EventUserRating.objects.filter(event_id=self.pk)
        summ = 0
        for r in reviews:
            summ += r.rating
        count = 1 if reviews.count() == 0 else reviews.count()
        return round(summ/count, 2)

    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        ans = send_mail(self.host.username, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Tag(core_models.TimeStampedModel):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    title = models.CharField(max_length=30, verbose_name="название")

    def __str__(self):
        return f"{self.title}"


class EventUserRating(models.Model):
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reviews", null=True, verbose_name="мероприятие")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", null=True, verbose_name="пользователь")
    rating = models.IntegerField(default=1, verbose_name="оценка")
    text = models.TextField(blank=True, null=True, verbose_name="комментарий")
    show = models.BooleanField(default=False)

    def __str__(self):
        return f"user: {self.user.pk, self.user.username} event: {self.event.pk}"
