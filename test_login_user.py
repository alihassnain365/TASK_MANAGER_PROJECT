from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def test_login_wrong_password():
    response = client.post("/login", json={"user_name":"ali", "password":"wrong"})
    response.status_code = 401 # 401 invalid credentials

def test_login_correct_password():
    response = client.post("/login", json={"user_name":"ali", "password":"ali"})
    assert response.status_code == 200
    assert "access_token" in response.json() # check if the access token mean the token is in hte json 
    