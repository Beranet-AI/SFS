import asyncio
from typing import AsyncGenerator
from backend.services.alerting.domain.events import LiveEvent


class EventBus:
    def __init__(self):
        self.subscribers: list[asyncio.Queue] = []

    async def publish(self, event: LiveEvent):
        for queue in self.subscribers:
            await queue.put(event)

    async def subscribe(self) -> AsyncGenerator[LiveEvent, None]:
        queue: asyncio.Queue = asyncio.Queue()
        self.subscribers.append(queue)
        try:
            while True:
                event = await queue.get()
                yield event
        finally:
            self.subscribers.remove(queue)


event_bus = EventBus()
