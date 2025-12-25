from django.db import models

class RuleModel(models.Model):
    """
    Rule های دستی و AI-suggested یک جا.
    action می‌تواند:
      - create_incident
      - send_command
    """
    name = models.CharField(max_length=150)
    is_enabled = models.BooleanField(default=True)

    # scope
    device_type = models.CharField(max_length=64, null=True, blank=True)
    metric = models.CharField(max_length=64, null=True, blank=True)

    # condition: {"op": ">", "value": 25}
    condition = models.JSONField(default=dict)

    # action: {"type":"create_incident", "severity":"high", "title":"...", "command": {...}}
    action = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
