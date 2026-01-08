import os
import time
import traceback
import django

# -------------------------------------------------
# 1️⃣ تنظیم محیط Django (باید اول باشد)
# -------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

# -------------------------------------------------
# 2️⃣ importها بعد از django.setup
# -------------------------------------------------
from apps.commands.infrastructure.models import CommandModel
from apps.commands.application.services.command_dispatcher import CommandDispatcher


def main(interval: int = 5, batch_size: int = 5):
    print("🟢 Commands Worker started")
    print("🔗 EDGE_CONTROLLER_BASE_URL =", os.getenv("EDGE_CONTROLLER_BASE_URL"))

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

                # ✅ فقط این
                dispatcher.dispatch(command.id)

            except Exception:
                # ❗ اینجا فقط log می‌کنیم
                # status و attempt داخل dispatcher مدیریت می‌شود
                print("❌ WORKER ERROR")
                print(traceback.format_exc())

        time.sleep(interval)


if __name__ == "__main__":
    main()
