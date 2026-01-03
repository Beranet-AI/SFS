import json
from pathlib import Path
from jsonschema import validate, ValidationError

# ======================================
# Base directory: backend/
# ======================================
BASE_DIR = Path(__file__).resolve().parents[4]

# ======================================
# Telemetry schema path
# backend/shared/schemas/management/telemetry/raw_telemetry_input.v1.json
# ======================================
SCHEMA_PATH = (
    BASE_DIR
    / "shared"
    / "schemas"
    / "management"
    / "telemetry"
    / "raw_telemetry_input.v1.json"
)

_schema_cache: dict | None = None


def _load_schema() -> dict:
    global _schema_cache

    if _schema_cache is None:
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(
                f"Telemetry schema not found: {SCHEMA_PATH}"
            )

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            _schema_cache = json.load(f)

    return _schema_cache


def validate_telemetry_payload(payload: dict) -> None:
    """
    Validate incoming telemetry payload against JSON Schema
    """
    schema = _load_schema()

    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid telemetry payload: {e.message}")
