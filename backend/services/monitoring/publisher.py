from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def publish_live_status(status: dict):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "live_status",
        {
            "type": "send_live_status",
            "live_status": status,
        },
    )
