"""Test configuration for the alerting service."""

from __future__ import annotations

import sys
from pathlib import Path


SERVICE_ROOT = Path(__file__).resolve().parents[1]
if SERVICE_ROOT.as_posix() not in sys.path:
    sys.path.insert(0, SERVICE_ROOT.as_posix())
