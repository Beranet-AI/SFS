from typing import Dict, Any, List, Optional
from datetime import datetime

class LiveStatusRepo:
    """
    نسخه ساده: in-memory
    در نسخه production می‌تونی Redis / TimescaleDB جایگزین کنی.
    """
    def __init__(self) -> None:
        self._latest_by_key: Dict[str, Dict[str, Any]] = {}

    def upsert_metric(self, key: str, metric: str, value: Any, base: Dict[str, Any]) -> Dict[str, Any]:
        row = self._latest_by_key.get(key) or {
            "ts": base["ts"],
            "device_id": base["device_id"],
            "device_type": base["device_type"],
            "farm_id": base.get("farm_id"),
            "barn_id": base.get("barn_id"),
            "zone_id": base.get("zone_id"),
            "livestock_id": base.get("livestock_id"),
            "metrics": {},
        }
        row["ts"] = base["ts"]
        row["metrics"][metric] = value
        self._latest_by_key[key] = row
        return row

    def list(self, livestock_id: Optional[str] = None) -> List[Dict[str, Any]]:
        rows = list(self._latest_by_key.values())
        if livestock_id:
            rows = [r for r in rows if r.get("livestock_id") == livestock_id]
        rows.sort(key=lambda r: r.get("ts", ""), reverse=True)
        return rows
