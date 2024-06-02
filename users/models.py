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

    avatar = models.ImageField(blank=True, upload_to="users_photos", verbose_name="аватар")
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10, blank=True, verbose_name="пол")
    bio = models.TextField(blank=True, verbose_name="краткая информация")
    birthdate = models.DateField(blank=True, null=True, verbose_name="дата рождения")
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default="Russian", verbose_name="язык")
    superhost = models.BooleanField(default=False, verbose_name="организатор")

    # def get_absolute_url(self):
    #     return reverse("users:profile", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})


class OrgForm(core_models.TimeStampedModel):
    class Meta:
        verbose_name = "форма организатора"
        verbose_name_plural = "формы организаторов"

    STATUS_PENDING = "pending"
    STATUS_CONFIRM = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRM, "Confirm"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING, verbose_name="статус")
    user = models.ForeignKey(User, related_name="org_form", on_delete=models.CASCADE, verbose_name="пользователь")
    organization = models.CharField(max_length=100, null=True, blank=True, verbose_name="организация")
    name = models.CharField(max_length=20, null=False, verbose_name="имя")
    last_surname = models.CharField(max_length=20, null=False, verbose_name="отчество")
    surname = models.CharField(max_length=20, null=False, verbose_name="фамилия")
    
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.status == "confirmed":
            self.user.superhost = True
            self.user.save()
        return super(OrgForm, self).save()

    def __str__(self):
        return f"{self.user.username}"