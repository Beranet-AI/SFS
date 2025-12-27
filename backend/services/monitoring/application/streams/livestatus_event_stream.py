from __future__ import annotations

import asyncio
from typing import AsyncIterator

from backend.shared.dto.livestatus_dto import LiveStatusEventDTO


class LiveStatusEventStream:
    """
    In-process pub/sub stream for SSE consumers.
    Later we can switch this to Redis Streams / NATS / Kafka.
    """

    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def publish(self, event: LiveStatusEventDTO) -> None:
        async with self._lock:
            for q in list(self._subscribers):
                # non-blocking best effort
                if q.full():
                    continue
                q.put_nowait(event.model_dump())

    async def subscribe(self) -> AsyncIterator[dict]:
        q: asyncio.Queue = asyncio.Queue(maxsize=200)
        async with self._lock:
            self._subscribers.add(q)

        try:
            while True:
                item = await q.get()
                yield item
        finally:
            async with self._lock:
                self._subscribers.discard(q)
