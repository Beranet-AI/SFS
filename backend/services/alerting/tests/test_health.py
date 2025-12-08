from __future__ import annotations

from fastapi.testclient import TestClient

<<<<<<< HEAD
from infrastructure.app import create_app
=======
from app.main import create_app
>>>>>>> origin/main


def test_health_endpoint_returns_status_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "alerting service is healthy",
    }
