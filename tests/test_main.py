from fastapi.testclient import TestClient

from main import app


def test_home_page_renders_successfully():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "WebSocket Chat" in response.text
