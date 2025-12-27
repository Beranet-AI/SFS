# backend/services/edge_controller/api/routes.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
import os
import uuid

from backend.services.edge_controller.application.services.command_executor import CommandExecutor
from backend.services.edge_controller.infrastructure.clients.monitoring_client import MonitoringClient

router = APIRouter()

MONITORING_BASE_URL = os.getenv("MONITORING_BASE_URL", "http://monitoring:8002")
monitoring = MonitoringClient(MONITORING_BASE_URL)
executor = CommandExecutor()


class ExecuteCommandIn(BaseModel):
    command_id: str
    attempt_no: int = Field(ge=1)
    command_name: str
    payload: dict = {}
    idempotency_key: str = ""


@router.post("/commands/execute")
def execute_command(body: ExecuteCommandIn, bg: BackgroundTasks):
    """
    Monitoring -> Edge: dispatch command

    Returns ACK immediately (fast).
    Sends RESULT asynchronously to Monitoring.
    """
    # ACK fast
    receipt = f"edge-receipt:{uuid.uuid4()}"
    try:
        monitoring.send_ack(
            command_id=body.command_id,
            attempt_no=body.attempt_no,
            executor_receipt=receipt,
            meta={"edge_node": os.getenv("EDGE_NODE_ID", ""), "note": "accepted"},
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"cannot ACK to monitoring: {e}")

    # Execute in background and post RESULT
    def _run():
        try:
            res = executor.execute(body.command_name, body.payload)
            monitoring.send_result(
                command_id=body.command_id,
                attempt_no=body.attempt_no,
                status=res.status,
                result=res.result,
                error_code=res.error_code,
                error_message=res.error_message,
                meta={"executor_receipt": receipt},
            )
        except Exception as e:
            monitoring.send_result(
                command_id=body.command_id,
                attempt_no=body.attempt_no,
                status="failed",
                result={},
                error_code="edge_exception",
                error_message=str(e),
                meta={"executor_receipt": receipt},
            )

    bg.add_task(_run)
    return {"ok": True, "executor_receipt": receipt}
