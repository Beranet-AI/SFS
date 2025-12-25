from typing import Dict, Any, List
from apps.rules.models import RuleModel

class PolicyEngine:
    def evaluate(self, telemetry: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        telemetry: {device_type, metric, value, farm_id, zone_id, livestock_id, ...}
        خروجی: list of actions (incident/command)
        """
        actions: List[Dict[str, Any]] = []
        qs = RuleModel.objects.filter(is_enabled=True)

        dt = telemetry.get("device_type")
        metric = telemetry.get("metric")
        value = telemetry.get("value")

        for r in qs:
            if r.device_type and r.device_type != dt:
                continue
            if r.metric and r.metric != metric:
                continue

            cond = r.condition or {}
            op = cond.get("op")
            th = cond.get("value")

            if self._match(op, value, th):
                actions.append(r.action)

        return actions

    def _match(self, op: str, value: Any, th: Any) -> bool:
        try:
            if op == ">": return float(value) > float(th)
            if op == ">=": return float(value) >= float(th)
            if op == "<": return float(value) < float(th)
            if op == "<=": return float(value) <= float(th)
            if op == "==": return value == th
            if op == "!=": return value != th
        except Exception:
            return False
        return False
