from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.services.monitoring.core.config import settings
from backend.services.monitoring.infrastructure.repositories.heartbeat_repository import InMemoryHeartbeatRepository
from backend.services.monitoring.application.streams.livestatus_event_stream import LiveStatusEventStream
from backend.services.monitoring.infrastructure.clients.management_client import ManagementClient
from backend.services.monitoring.infrastructure.clients.command_client import CommandClient
from backend.services.monitoring.application.dispatchers.incident_dispatcher import IncidentDispatcher
from backend.services.monitoring.application.dispatchers.command_dispatcher import CommandDispatcher
from backend.services.monitoring.application.services.device_health_service import DeviceHealthService
from backend.services.monitoring.application.services.livestatus_service import LiveStatusService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Boot wiring (poor-man DI):
      - repositories
      - clients
      - streams
      - services
      - background offline-check loop
    """

    # Infrastructure
    heartbeat_repo = InMemoryHeartbeatRepository()
    mgmt_client = ManagementClient(base_url=settings.MANAGEMENT_BASE_URL)
    cmd_client = CommandClient(base_url=settings.EDGE_CONTROLLER_BASE_URL)

    # Streams
    livestatus_stream = LiveStatusEventStream()

    # Dispatchers
    incident_dispatcher = IncidentDispatcher(management_client=mgmt_client)
    command_dispatcher = CommandDispatcher(command_client=cmd_client)

    # Services
    device_health = DeviceHealthService(
        heartbeat_repo=heartbeat_repo,
        incident_dispatcher=incident_dispatcher,
        offline_threshold_seconds=settings.HEARTBEAT_OFFLINE_THRESHOLD_SECONDS,
    )
    livestatus_service = LiveStatusService(
        stream=livestatus_stream,
        incident_dispatcher=incident_dispatcher,
        command_dispatcher=command_dispatcher,
    )

    # Attach to app state
    app.state.heartbeat_repo = heartbeat_repo
    app.state.livestatus_stream = livestatus_stream
    app.state.device_health = device_health
    app.state.livestatus_service = livestatus_service

    stop_event = asyncio.Event()

    async def offline_checker_loop():
        while not stop_event.is_set():
            try:
                await device_health.offline_check_tick()
            except Exception:
                # never crash monitoring because of background loop
                pass
            await asyncio.sleep(settings.HEARTBEAT_CHECK_INTERVAL_SECONDS)

    task = asyncio.create_task(offline_checker_loop())

    try:
        yield
    finally:
        stop_event.set()
        task.cancel()
        try:
            await task
        except Exception:
            pass
