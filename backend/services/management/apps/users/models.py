from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from .managers import UserManager


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_number = models.CharField(max_length=32, blank=True, default="")
    is_active_account = models.BooleanField(default=True)

    objects = UserManager()

    class Meta:
        app_label = "users"
        db_table = "users_user"
