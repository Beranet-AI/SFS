import json

from channels.generic.websocket import AsyncWebsocketConsumer


class LiveStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_live_status(self, event):
        await self.send(text_data=json.dumps(event["live_status"]))
