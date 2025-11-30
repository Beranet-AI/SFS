import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensure a service account exists for inter-service authentication"

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_AUTH_USERNAME")
        password = os.getenv("DJANGO_AUTH_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_AUTH_USERNAME and DJANGO_AUTH_PASSWORD must be set to create the service user."
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"is_staff": True, "is_active": True},
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Created service user '{username}' with provided credentials.")
            )
            return

        if not user.check_password(password):
            user.set_password(password)
            user.save(update_fields=["password"])
            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated password for existing service user '{username}'."
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS(f"Service user '{username}' already exists."))
