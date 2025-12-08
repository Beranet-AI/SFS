"""Compatibility shim for alert service logic.

The application-layer implementation lives in
:mod:`management.application.alerts.service`. This module re-exports the
function to preserve import stability for existing callers under
``alerts.services``.
"""

from management.application.alerts.service import evaluate_alerts_for_reading

__all__ = ["evaluate_alerts_for_reading"]
