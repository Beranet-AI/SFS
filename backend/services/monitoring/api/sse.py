from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator, Callable, Optional

from fastapi import Request
from starlette.responses import StreamingResponse


def _format_sse(data: dict, event: Optional[str] = None) -> str:
    # SSE format: optional event, then data lines, then blank line.
    # Keep it robust for JSON payloads.
    payload = json.dumps(data, ensure_ascii=False)
    lines = []
    if event:
        lines.append(f"event: {event}")
    lines.append(f"data: {payload}")
    return "\n".join(lines) + "\n\n"


async def sse_stream(
    request: Request,
    iterator_factory: Callable[[], AsyncIterator[dict]],
    event_name: Optional[str] = None,
    ping_interval_seconds: int = 15,
) -> StreamingResponse:
    async def event_generator():
        # Keep-alive / ping prevents proxies from closing idle SSE connections.
        last_ping = 0.0
        iterator = iterator_factory()
        try:
            async for item in iterator:
                if await request.is_disconnected():
                    break
                yield _format_sse(item, event=event_name)

                # opportunistic ping scheduling (after a message)
                now = asyncio.get_event_loop().time()
                if now - last_ping >= ping_interval_seconds:
                    last_ping = now
                    yield _format_sse({"type": "ping"}, event="ping")
        except asyncio.CancelledError:
            return

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
