from django import forms

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from . import models


class SearchForm(forms.Form):
    title = forms.CharField(initial="")


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = (
            "title",
            "description",
            "online",
            "city",
            "street",
            "time_start",
            "time_end",
            "preview",
            "tags",
        )

        widgets = {
            "time_start": forms.DateTimeInput(),
            "time_end": forms.DateTimeInput(),
        }

    def save(self, *args, **kwargs):
        event = super().save(commit=False)
        return event


class CreateReviewForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = models.EventUserRating
        fields = (
            "text",
            "rating",
        )

    def save(self):
        review = super().save(commit=False)
        return review
