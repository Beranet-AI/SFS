import os

env = os.getenv("DJANGO_SETTINGS_ENV", "").lower()

if env == "prod":
    from .prod import *  # noqa: F401,F403
elif env == "test":
    from .test import *  # noqa: F401,F403
elif env == "dev":
    from .dev import *  # noqa: F401,F403
else:
    from .base import *  # noqa: F401,F403

