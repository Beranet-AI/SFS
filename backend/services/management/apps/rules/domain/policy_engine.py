"""
Policy Engine: orchestrates which rules/policies should run.
Still NO database access here.
"""

from apps.rules.domain.rules_catalog import RULES

class PolicyEngine:
    def list_rules(self):
        return RULES
