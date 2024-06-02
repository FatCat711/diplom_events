from urllib.request import Request

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, UpdateView

from .models import User, OrgForm
from . import forms, mixins


class ProfileView(View):
    def get(self, request: Request, pk):
        user = User.objects.get(id=pk)
        org_form = OrgForm.objects.get_or_none(user=user)
        return render(request, "users/user_detail.html", context={
            "user": user,
            "org_form": org_form,
        })


class UserProfileUpdate(SuccessMessageMixin, UpdateView):
    success_message = "Profile updated"
    model = User
    template_name = "users/update-profile.html"
    fields = [
        "email",
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
    ]

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["email"].widget.attrs = {"placeholder": "Email"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First_name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last_name"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["language"].widget.attrs = {"placeholder": "Language"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        return form

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        self.object.username = email
        self.object.save()
        return super().form_valid(form)


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user: User = authenticate(
            self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogInView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def get_success_url(self):
        return reverse("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("core:home"))


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update-password.html"
    success_message = "Пароль изменен"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class CreateOrgFormView(mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateOrgFormForm
    template_name = "mixins/org/org_form_create.html"

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        if user.org_form.exists():
            if user.org_form.status != "canceled":
                return redirect(reverse("users:profile", kwargs={"pk": user.pk}))
        org_form = form.save()
        org_form.user = user
        org_form.save()
        return redirect(reverse("users:profile", kwargs={"pk": user.pk}))
