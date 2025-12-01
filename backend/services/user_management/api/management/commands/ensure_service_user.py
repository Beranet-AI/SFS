from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create or update the inter-service API user (for FastAPI → Django)."

    def handle(self, *args, **kwargs):
        username = os.getenv("DJANGO_AUTH_USERNAME")
        password = os.getenv("DJANGO_AUTH_PASSWORD")

        if not username or not password:
            self.stderr.write(
                "DJANGO_AUTH_USERNAME and DJANGO_AUTH_PASSWORD must be set"
            )
            return

        user, created = User.objects.update_or_create(
            username=username,
            defaults={"is_staff": True, "is_superuser": True},
        )

        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(f"Created new service user: {username}")
        else:
            self.stdout.write(f"Updated existing service user: {username}")
