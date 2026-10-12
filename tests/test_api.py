
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert "/api/gold/latest" in data["endpoints"]


def test_latest_gold_rate():
    response = client.get("/api/gold/latest")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["city"] == "Chennai"
    assert data["data"]["rate_24k"] > 0
    assert data["data"]["rate_22k"] > 0


def test_gold_history():
    response = client.get("/api/gold/history?limit=5")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["count"] <= 5
    assert len(data["data"]) == data["count"]


def test_gold_analysis():
    response = client.get("/api/gold/analysis")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["24k"]["movement"] in [
        "increased",
        "decreased",
        "unchanged"
    ]
    assert data["22k"]["movement"] in [
        "increased",
        "decreased",
        "unchanged"
    ]


def test_invalid_history_limit():
    response = client.get("/api/gold/history?limit=500")

    assert response.status_code == 422


def test_unknown_city():
    response = client.get(
        "/api/gold/latest?city=UnknownCity"
    )

    assert response.status_code == 404
