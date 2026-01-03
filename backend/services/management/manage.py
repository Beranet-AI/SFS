#!/usr/bin/env python
import os
import sys
from pathlib import Path

# ⬇️ تعیین ریشه‌ی واقعی پروژه: backend/
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()

