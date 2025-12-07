"""Test configuration for data_ingestion service."""

from __future__ import annotations

import sys
from pathlib import Path


# Ensure the service package is importable when running tests from the repo root.
SERVICE_ROOT = Path(__file__).resolve().parents[1]
if SERVICE_ROOT.as_posix() not in sys.path:
    sys.path.insert(0, SERVICE_ROOT.as_posix())

