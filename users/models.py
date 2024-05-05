from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from core import models as core_models


class User(AbstractUser):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_RUSSIAN = "ru"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_RUSSIAN, "Russian"),
    )

    avatar = models.ImageField(blank=True, upload_to="users_photos")
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default="Russian")
    superhost = models.BooleanField(default=False)

    # def get_absolute_url(self):
    #     return reverse("users:profile", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})


class OrgForm(core_models.TimeStampedModel):

    STATUS_PENDING = "pending"
    STATUS_CONFIRM = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRM, "Confirm"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING)
    user = models.ForeignKey(User, related_name="org_form", on_delete=models.CASCADE)
    organization = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=20, null=False)
    last_surname = models.CharField(max_length=20, null=False)
    surname = models.CharField(max_length=20, null=False)
    
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.status == "confirmed":
            self.user.superhost = True
            self.user.save()
        return super(OrgForm, self).save()

    def __str__(self):
        return f"{self.user.username}"