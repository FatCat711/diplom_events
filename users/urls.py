from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("login/", views.LogInView.as_view(), name="login"),
    path("logout/", views.LogOutView.as_view(), name="logout"),
    path("profile/<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("update-profile/", views.UserProfileUpdate.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
    path("org/", views.CreateOrgFormView.as_view(), name="org_create"),
]

