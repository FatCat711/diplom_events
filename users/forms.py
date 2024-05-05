from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            self.add_error("password", forms.ValidationError("Password is incorrect"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("USer does not exist"))


class SignUpForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
                                attrs={"placeholder": "Confirm password"}))

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password", error)
        password1 = self.cleaned_data.get("password1")
        if password1 != password1:
            raise forms.ValidationError("Password does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        user.username = email
        user.set_password(password)
        user.save()


class CreateOrgFormForm(forms.ModelForm):
    class Meta:
        model = models.OrgForm
        fields = (
            "organization",
            "name",
            "last_surname",
            "surname",
        )

    def save(self, *args, **kwargs):
        org_form = super().save(commit=False)
        return org_form
