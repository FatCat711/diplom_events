import datetime

from django.utils import timezone
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, UpdateView, FormView
from .partials import mail

from . import forms
from . import models
from users.models import User
from users import mixins as user_mixins


class EventDetailView(View):
    def get(self, request, pk):
        flag = False
        review_flag = False

        event = models.Event.objects.get(pk=pk)
        try:
            user = User.objects.get(pk=request.user.pk)
            if user in event.participants.all():
                flag = True
            if event.time_end < timezone.now() and event in user.events.all():
                review_flag = True
        except Exception:
            pass
        return render(request, "events/detail.html", context={
            "event": event,
            "flag": flag,
            "review_flag": review_flag,
            "reviews": event.reviews.filter(show=True)
        })


def event_register(request, pk):
    event = models.Event.objects.get(pk=pk)
    try:
        user = User.objects.get(pk=request.user.pk)
        if user not in event.participants.all():
            event.participants.add(user)
            rating, created = models.EventUserRating.objects.get_or_create(user=user, event=event)
            if created:
                rating.rating = 5
                rating.show = False
                rating.save()
        else:
            event.participants.remove(user)
            rating, created = models.EventUserRating.objects.get_or_create(user=user, event=event)
            if not created:
                rating.delete()
    except Exception:
        return redirect(reverse("users:login"))
    return redirect(reverse("events:detail", kwargs={"pk": pk}))


class EventListView(ListView):
    model = models.Event
    paginate_by = 12
    paginate_orphans = 5
    page_kwarg = "page"
    ordering = "created"
    context_object_name = "events"
    template_name = "events/event_list.html"


class EditEventView(UpdateView):
    model = models.Event
    fields = [
        "title",
        "description",
        "online",
        "city",
        "street",
        "time_start",
        "time_end",
        "tags",
        "preview",
    ]
    template_name = "events/event_edit.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

from events.tasks import send_review_email_task

class CreateEventView(user_mixins.LoggedInOnlyView, FormView):
    form_class = forms.CreateRoomForm
    template_name = "events/event_create.html"

    def form_valid(self, form):
        event = form.save()
        event.host = User.objects.get(pk=self.request.user.pk)
        event.save()
        event.participants.add(User.objects.get(pk=self.request.user.pk))
        form.save_m2m()
        send_review_email_task.delay(event.host.email, event.title)
        return redirect(reverse("events:detail", kwargs={"pk": event.pk}))


def create_review(request, pk):
    if request.method == "GET":
        event = models.Event.objects.get(pk=pk)
        form = forms.CreateReviewForm()
        return render(request,
                      "events/review_add.html",
                      context={
                          "event": event,
                          "form": form,
                      })
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        event: models.Event = models.Event.objects.get_or_none(pk=pk)
        if not event and event.time_end > datetime.datetime.now():
            return redirect(reverse("core:home"))
        if form.is_valid():
            try:
                review = models.EventUserRating.objects.get(event=event, user=request.user)
                review.delete()
            except Exception:
                pass
            try:
                user = User.objects.get(pk=request.user.pk)
            except Exception:
                redirect(reverse("users:login"))
            review = form.save()
            review.event = event
            review.user = request.user
            review.show = True
            review.save()
            return redirect(reverse("events:detail", kwargs={"pk": event.pk}))
        return redirect(reverse("events:detail", kwargs={"pk": event.pk}))


class SearchView(View):
    def get(self, request):
        title = request.GET.get("title")
        if title:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                title = form.cleaned_data.get("title")
                qs = models.Event.objects.filter(title__istartswith=title)
                print(qs)
                return render(request,
                              "events/search.html",
                              context={
                                  "query": title,
                                  "events": qs,
                                  "form": form,
                              })
        else:
            return redirect(reverse("core:home"))


class EventDelete(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=request.user.pk)
            event = models.Event.objects.get(pk=pk)
            if event.host.pk == user.pk:
                event.delete()
            return redirect(reverse("core:home"))
        except Exception:
            return redirect(reverse("core:home"))
