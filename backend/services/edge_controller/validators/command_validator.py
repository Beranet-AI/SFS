import json
from pathlib import Path
from jsonschema import validate, ValidationError

# مسیر پایه shared
BASE_DIR = Path(__file__).resolve().parents[3]  # backend/
SCHEMA_PATH = (
    BASE_DIR
    / "shared"
    / "schema"
    / "edge_controller"
    / "command"
    / "input.v1.json"
)

_schema_cache: dict | None = None


def _load_schema() -> dict:
    global _schema_cache

    if _schema_cache is None:
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(
                f"Command schema not found: {SCHEMA_PATH}"
            )

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            _schema_cache = json.load(f)

    return _schema_cache


def validate_command_payload(payload: dict) -> None:
    """
    Validate incoming command payload against JSON Schema
    """
    schema = _load_schema()

    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid command payload: {e.message}")
