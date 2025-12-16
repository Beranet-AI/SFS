import asyncio
from typing import AsyncGenerator

from backend.services.monitoring.domain.live_status import LiveStatusEvent


class EventBus:
    def __init__(self):
        self.subscribers: list[asyncio.Queue] = []

    async def publish(self, event: LiveStatusEvent):
        for queue in self.subscribers:
            await queue.put(event)

    async def subscribe(self) -> AsyncGenerator[LiveStatusEvent, None]:
        queue: asyncio.Queue = asyncio.Queue()
        self.subscribers.append(queue)
        try:
            while True:
                event = await queue.get()
                yield event
        finally:
            self.subscribers.remove(queue)


event_bus = EventBus()
