import json
from fastapi import Request
from fastapi.responses import StreamingResponse
from shared.dto.realtime_event_dto import RealtimeEventDTO
from backend.services.monitoring.application.streams.livestatus_event_stream import EventStream

event_stream = EventStream()

async def sse_generator(request: Request):
    async for event in event_stream.subscribe():
        if await request.is_disconnected():
            break

        data = json.dumps(event.__dict__, default=str)
        yield f"data: {data}\n\n"

def sse_endpoint(request: Request):
    return StreamingResponse(
        sse_generator(request),
        media_type="text/event-stream",
    )
