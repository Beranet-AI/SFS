from django.core.management.base import BaseCommand

from apps.commands.application.workers.run_commands_worker import run_worker


class Command(BaseCommand):
    help = "Run commands worker loop"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--interval",
            type=int,
            default=5,
            help="Sleep interval between polling cycles (seconds).",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=5,
            help="Number of pending commands to dispatch per cycle.",
        )

    def handle(self, *args, **options) -> None:
        interval = int(options["interval"])
        batch_size = int(options["batch_size"])
        run_worker(interval=interval, batch_size=batch_size)
