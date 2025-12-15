import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.services.alerting.application.event_bus import event_bus

router = APIRouter()


@router.get("/stream")
async def stream_events():
    async def event_generator():
        async for event in event_bus.subscribe():
            yield f"data: {event.model_dump_json()}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
