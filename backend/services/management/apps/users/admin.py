from django.contrib import admin
from .models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_active")
    search_fields = ("email",)
