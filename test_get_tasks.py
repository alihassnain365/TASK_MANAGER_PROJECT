from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def test_get_task_without_token():
    response = client.get("/tasks")
    assert response.status_code == 401 # 401 mean that you are unauthorized
    
