import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv

User = get_user_model()


class Command(BaseCommand):
    help = "Create or update the inter-service API user (for FastAPI → Django)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            dest="username",
            help="Override the username for the service user (defaults to DJANGO_AUTH_USERNAME)",
        )
        parser.add_argument(
            "--password",
            dest="password",
            help="Override the password for the service user (defaults to DJANGO_AUTH_PASSWORD)",
        )

    def handle(self, *args, **kwargs):
        # Load env files if present so local runs (outside docker-compose) still work
        base_dir = Path(settings.BASE_DIR)
        load_dotenv(base_dir / ".env", override=False)
        load_dotenv(base_dir / ".env.docker", override=False)

        username = kwargs.get("username") or os.getenv("DJANGO_AUTH_USERNAME")
        password = kwargs.get("password") or os.getenv("DJANGO_AUTH_PASSWORD")
        email = os.getenv("DJANGO_AUTH_EMAIL", f"{username or 'service'}@local")

        if not username or not password:
            raise CommandError(
                "DJANGO_AUTH_USERNAME and DJANGO_AUTH_PASSWORD must be set (env or --username/--password) to create the service user."
            )

        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "email": email,
                "is_active": True,
            },
        )

        user.set_password(password)
        user.save(update_fields=["password", "is_staff", "is_superuser", "email", "is_active"])

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new service user: {username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated existing service user: {username}"))
