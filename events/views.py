from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, UpdateView, FormView

from . import forms
from . import models
from events.partials import svd
from users.models import User
from users import mixins as user_mixins


class EventDetailView(View):
    def get(self, request, pk):
        flag = False
        event = models.Event.objects.get(pk=pk)
        try:
            user = User.objects.get(pk=request.user.pk)
            if user in event.participants.all():
                flag = True
        except Exception:
            pass
        return render(request, "events/detail.html", context={
            "event": event,
            "flag": flag,
        })


def event_register(request, pk):
    event = models.Event.objects.get(pk=pk)
    try:
        user = User.objects.get(pk=request.user.pk)
        if user not in event.participants.all():
            event.participants.add(user)
            event.save()
        else:
            event.participants.remove(user)
            event.save()
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


class SearchView(View):
    def get(self, request):
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            free = form.cleaned_data.get("free")
            online = form.cleaned_data.get("online")
            tags = form.cleaned_data.get("tags")

            filter_args = {}

            if title != "A":
                filter_args["city__startswith"] = title

            if tags is not None:
                filter_args["tags"] = tags

            if free:
                filter_args["free"] = True

            if online:
                filter_args["online"] = True

            for tag in tags:
                filter_args["tags"] = tag

            qs = models.Event.objects.filter(
                **filter_args).order_by("-created")

            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)

            events = paginator.get_page(page)

            return render(request, "", context={
                "form": form,
                "rooms": events,
            })
        return render(request, "", context={
            "form": form,
        })


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


class CreateEventView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "events/event_create.html"

    def form_valid(self, form):
        event = form.save()
        event.host = User.objects.get(pk=self.request.user.pk)
        event.save()
        event.participants.add(User.objects.get(pk=self.request.user.pk))
        form.save_m2m()
        return redirect(reverse("events:detail", kwargs={"pk": event.pk}))
