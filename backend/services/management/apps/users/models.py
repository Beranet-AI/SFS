from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    """
    Canonical Django ORM model for users.
    DDD: Infrastructure adapter for User domain entity.
    """
    pass
