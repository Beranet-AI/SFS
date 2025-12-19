from django.db import models

class UserModel(models.Model):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.email
