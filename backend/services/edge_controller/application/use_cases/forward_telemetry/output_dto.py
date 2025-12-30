from dataclasses import dataclass


@dataclass(frozen=True)
class ForwardTelemetryOutputDTO:
    forwarded: bool
