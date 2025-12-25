import asyncio
import json
from typing import AsyncGenerator, Dict, Any, Optional
from fastapi import Request


class LiveStatusEventStream:
    """
    SSE stream: yields 'data: <json>\\n\\n'
    """
    def __init__(self):
        self._queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue(maxsize=2000)

    async def publish(self, evt: Dict[str, Any]) -> None:
        # avoid blocking if slow clients
        try:
            self._queue.put_nowait(evt)
        except asyncio.QueueFull:
            # drop oldest behavior could be implemented; here we just drop
            pass

    async def subscribe(self, request: Request, livestock_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        while True:
            if await request.is_disconnected():
                break
            evt = await self._queue.get()
            if livestock_id and evt.get("livestock_id") != livestock_id:
                continue
            yield f"data: {json.dumps(evt, ensure_ascii=False)}\n\n"
