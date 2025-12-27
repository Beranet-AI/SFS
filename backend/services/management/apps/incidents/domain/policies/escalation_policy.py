from backend.shared.enums.incident_severity import IncidentSeverity

class EscalationPolicy:
    """
    Decides escalation actions based on severity.
    """

    @staticmethod
    def should_escalate(severity: IncidentSeverity) -> bool:
        return severity in (
            IncidentSeverity.HIGH,
            IncidentSeverity.CRITICAL,
        )
