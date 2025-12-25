from django.db import models

class CommandModel(models.Model):
    """
    دستورهایی که به actuatorها ارسال می‌شود.
    source: manual/policy/ai
    status: queued/sent/ack/failed
    """
    target_device_id = models.IntegerField()
    command_type = models.CharField(max_length=80)
    payload = models.JSONField(default=dict, blank=True)
    source = models.CharField(max_length=16, default="manual")
    status = models.CharField(max_length=16, default="queued")
    created_at = models.DateTimeField(auto_now_add=True)
