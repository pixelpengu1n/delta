from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_greet():
    response = client.get("/greet")
    assert response.status_code == 200
    assert response.json() == "Welcome to Delta Finances"
