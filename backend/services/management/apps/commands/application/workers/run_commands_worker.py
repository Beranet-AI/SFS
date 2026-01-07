import os
import time
import django
import traceback

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.dev",
)

django.setup()

from apps.commands.infrastructure.models import CommandModel
from apps.commands.application.services.command_dispatcher import CommandDispatcher


def main(interval: int = 5, batch_size: int = 5):
    print("🟢 Commands Worker started")
    print("🔗 EDGE_CONTROLLER_BASE_URL=", os.getenv("EDGE_CONTROLLER_BASE_URL"))

    dispatcher = CommandDispatcher()

    while True:
        pending = (
            CommandModel.objects
            .filter(status="pending")
            .order_by("created_at")[:batch_size]
        )

        print(f"🔎 Pending commands: {pending.count()}")

        for command in pending:
            try:
                print(f"➡️ Dispatching command {command.id}")

                dispatcher.dispatch_to_edge(
                    command_id=str(command.id),
                    command_name=command.command_name,
                    edge_id=command.target_id,
                    payload=command.payload,
                )

                command.status = "dispatched"
                command.save(update_fields=["status"])

            except Exception as exc:
                tb = traceback.format_exc()
                print("❌ WORKER ERROR")
                print(tb)

                command.last_error_message = str(exc)
                command.last_result = {"traceback": tb}
                command.status = "failed"
                command.save(update_fields=[
                    "last_error_message",
                    "last_result",
                    "status",
                ])

        time.sleep(interval)


if __name__ == "__main__":
    main()
