import pytest
from unittest.mock import patch
import app as flask_app

@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with patch("app.r") as mock_redis:
        mock_redis.incr.return_value = 42
        mock_redis.get.return_value = "42"
        with flask_app.app.test_client() as c:
            yield c

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["visits"] == 42

def test_reset(client):
    res = client.post("/reset")
    assert res.status_code == 200
    assert res.get_json()["visits"] == 0

def test_stats(client):
    res = client.get("/stats")
    assert res.status_code == 200
