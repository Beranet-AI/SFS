# Import all route modules so they register themselves
from . import command
from . import management_telemetry  # registers telemetry route
# heartbeat لازم نیست چون مستقیم در main include شده
