import os

os.environ["PYTHONHASHSEED"] = "0"

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_log_level_is_detected():
    response = client.post(
        "/logs",
        json={"message": "Database connection failed", "source": "api"},
    )
    assert response.status_code == 201
    assert response.json()["level"] == "ERROR"


def test_filter_and_stats():
    client.post("/logs", json={"message": "Server started", "source": "api"})
    client.post("/logs", json={"message": "Slow request warning", "source": "api"})
    client.post("/logs", json={"message": "Payment failed", "source": "payments"})

    errors = client.get("/logs?level=ERROR")
    assert errors.status_code == 200
    assert len(errors.json()) == 1

    stats = client.get("/stats")
    assert stats.status_code == 200
    body = stats.json()
    assert body["total"] == 3
    assert body["info"] == 1
    assert body["warning"] == 1
    assert body["error"] == 1
