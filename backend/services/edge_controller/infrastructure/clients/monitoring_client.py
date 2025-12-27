# backend/services/edge_controller/infrastructure/clients/monitoring_client.py
import requests


class MonitoringClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def send_ack(self, command_id: str, attempt_no: int, executor_receipt: str = "", meta: dict | None = None):
        payload = {
            "command_id": command_id,
            "attempt_no": attempt_no,
            "executor_receipt": executor_receipt,
            "meta": meta or {},
        }
        r = requests.post(f"{self.base_url}/commands/ack", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()

    def send_result(self, command_id: str, attempt_no: int, status: str, result: dict | None = None,
                    error_code: str = "", error_message: str = "", meta: dict | None = None):
        payload = {
            "command_id": command_id,
            "attempt_no": attempt_no,
            "status": status,
            "result": result or {},
            "error_code": error_code,
            "error_message": error_message,
            "meta": meta or {},
        }
        r = requests.post(f"{self.base_url}/commands/result", json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
