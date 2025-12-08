from fastapi.testclient import TestClient

from infrastructure.app import create_app


def test_health_endpoint_returns_status_ok():
    client = TestClient(create_app())

    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "data_ingestion service is healthy",
    }
