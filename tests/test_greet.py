from fastapi.testclient import TestClient

from src.lambda_function import app

client = TestClient(app)


def test_greet():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Delta Finances"
