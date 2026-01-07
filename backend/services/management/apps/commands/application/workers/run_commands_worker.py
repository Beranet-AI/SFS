import logging
import os
import time

from django.db import close_old_connections

from apps.commands.application.services.command_dispatcher import CommandDispatcher
from apps.commands.infrastructure.models import CommandModel

logger = logging.getLogger(__name__)


def run_worker(*, interval: int = 5, batch_size: int = 5) -> None:
    logger.info("Commands worker started")
    logger.info(
        "EDGE_CONTROLLER_BASE_URL=%s",
        os.getenv("EDGE_CONTROLLER_BASE_URL"),
    )

    dispatcher = CommandDispatcher()

    while True:
        close_old_connections()

        pending = list(
            CommandModel.objects
            .filter(status="pending")
            .order_by("created_at")[:batch_size]
        )

        logger.info("Pending commands: %s", len(pending))

        for command in pending:
            try:
                logger.info("Dispatching command %s", command.id)
                dispatcher.dispatch(command_id=str(command.id))
            except Exception as exc:
                logger.exception("WORKER ERROR")
                command.last_error_message = str(exc)
                command.last_result = {"error": str(exc)}
                command.status = "failed"
                command.save(
                    update_fields=[
                        "last_error_message",
                        "last_result",
                        "status",
                    ]
                )

        time.sleep(interval)


def main(interval: int = 5, batch_size: int = 5) -> None:
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.worker")
    django.setup()
    run_worker(interval=interval, batch_size=batch_size)


if __name__ == "__main__":
    main()
