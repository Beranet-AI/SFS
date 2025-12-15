from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def publish_alert(alert: dict):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "alerts",
        {
            "type": "send_alert",
            "alert": alert,
        },
    )
