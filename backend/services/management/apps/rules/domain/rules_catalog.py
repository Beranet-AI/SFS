"""
Rules Catalog: registry of rule names and metadata.
No persistence here; rules are code or can be loaded from config later.
"""

RULES = {
    "health.evaluate": {
        "description": "Evaluates health score into HealthState",
        "version": "1.0",
    },
    "incident.trigger": {
        "description": "Triggers incident when thresholds exceeded",
        "version": "1.0",
    },
}
