from django import forms
from . import models


# class SearchForm(forms.Form):
#
#     city = forms.CharField(initial="Anywhere")
#     room_type = forms.ModelChoiceField(
#         required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
#     )
#     price = forms.IntegerField(required=False)
#     guests = forms.IntegerField(required=False)
#     bedrooms = forms.IntegerField(required=False)
#     beds = forms.IntegerField(required=False)
#     baths = forms.IntegerField(required=False)
#     instant_book = forms.BooleanField(required=False)
#     superhost = forms.BooleanField(required=False)
#     amenities = forms.ModelMultipleChoiceField(
#         required=False,
#         queryset=models.Amenity.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#     )
#     facilities = forms.ModelMultipleChoiceField(
#         required=False,
#         queryset=models.Facility.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#     )
#
#
# class CreatePhotoForm(forms.ModelForm):
#     class Meta:
#         model = models.Photo
#         fields = ("caption", "file")
#
#     def save(self, pk, *args, **kwargs):
#         photo = super().save(commit=False)
#         room = models.Room.objects.get(pk=pk)
#         photo.room = room
#         photo.save()
#
#
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

    def save(self, *args, **kwargs):
        event = super().save(commit=False)
        return event
