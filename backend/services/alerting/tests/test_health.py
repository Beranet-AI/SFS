from __future__ import annotations
<<<<<<< HEAD
from fastapi.testclient import TestClient
=======

from fastapi.testclient import TestClient

>>>>>>> 6d8e73cf305191ad8ec89e17ac30b5bbc96c1d9a
from infrastructure.app import create_app


def test_health_endpoint_returns_status_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "alerting service is healthy",
    }
