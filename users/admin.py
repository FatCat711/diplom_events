from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile", {
            "fields": ("avatar", "gender", "bio",
                       "birthdate", "language",
                       "superhost")
        }),
    )

    list_filter = UserAdmin.list_filter + (
        "superhost",
    )

    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "superhost",
        "is_staff",
        "is_superuser",
    ]
