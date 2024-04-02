from django.contrib import admin

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "time_start", "time_end"]
    list_display_links = ["id", "title",]


@admin.register(models.EventUserRating)
class EventUserRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass
