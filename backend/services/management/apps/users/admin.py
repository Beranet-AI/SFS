from django.contrib import admin
from .infrastructure.models.user_model import UserModel

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "role", "is_active")
