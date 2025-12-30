# Import all route modules so they register themselves
from . import command
from . import telemetry  # اگر داری
# heartbeat لازم نیست چون مستقیم در main include شده
