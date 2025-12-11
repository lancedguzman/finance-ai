from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from . models import Profile

class ProfileInline(admin.StackedInline):
    """Creates the Profile Admin Panel."""
    model = Profile
    can_delete = False
    fields = ["user", "display_name",
              "email_address", "telegram_chat_id"]


class UserAdmin(BaseUserAdmin):
    """Sets how the Profiles are displayed in Admin Panel."""
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
