"""in this file we will test that the relevant user can change the relevant tasks"""
from fastapi.testclient import TestClient
from main_api import app
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_api import get_db
import os
from dotenv import load_dotenv



from models import Base
load_dotenv()

test_engine = create_engine(os.getenv("database_url"))
TestSession = sessionmaker(bind=test_engine)

def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

def get_token(username:str, password:str):
    response = client.post("/login", json={"user_name":username, "password":password})
    return response.json()["access_token"]

"""seed function"""
def seed_the_user():
    for name,username,pw in [("Ali Hassnain","ali","ali"),("Ihtisham","shami","shami")]:
        client.post("/signup", json={"full_name":name, "user_name":username, "password":pw})


@pytest.fixture(scope="session", autouse=True)
def fresh_database():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    seed_the_user()


@pytest.fixture
def ali_token():
    return get_token("ali","ali")

@pytest.fixture
def shami_token():
    return get_token("shami","shami")

def test_ali_cannot_access_shami_task(ali_token,shami_token):
    # shami logged in and created the task, whit shami_task_id
    create_task = client.post("/create/task", json={"title":"pray isha"}, headers={"Authorization": f"Bearer {shami_token}"})
    shami_task_id = create_task.json()["id"]

    # now ali is logged in and he would try to access shami_task_id
    response = client.patch(f"/mark_task/{shami_task_id}/complete", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 403 # i know who you are , but you are not allowed to do that


def test_ali_can_complete_his_task(ali_token):
    # ali is creating a task
    ali_task = client.post("/create/task", json={"title":"pray fajr"}, headers={"Authorization": f"Bearer {ali_token}"})
    ali_task_id = ali_task.json()["id"]

    # now ali is marking complete to his task
    response = client.patch(f"/mark_task/{ali_task_id}/complete", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 200
    assert response.json()["status"] == True
    
def test_ali_cannot_delete_shami_task(shami_token, ali_token):
    # shami login and create a task
    shami_task = client.post("/create/task", json={"title":"pray five times a day"}, headers={"Authorization": f"Bearer {shami_token}"})
    shami_task_id = shami_task.json()["id"]

    # ali login and try to delete the shami's task
    response = client.delete(f"/delete_task/{shami_task_id}", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 403 # i know you who you are but you are not allowed to do this

def test_ali_can_delete_his_own_task(ali_token):
    # ali login and creates a task
    ali_task = client.post("/create/task", json={"title":"do hardwork, allah will help you"}, headers={"Authorization": f"Bearer {ali_token}"})
    ali_task_id = ali_task.json()["id"]

    # now ali deletes his task
    response = client.delete(f"/delete_task/{ali_task_id}", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 204 # no return content
    response = client.get("/tasks", headers={"Authorization": f"Bearer {ali_token}"})
    ids_list = [task["id"] for task in response.json()]
    assert ali_task_id not in ids_list

def test_duplicate_signup():
    response = client.post("/signup", json={"full_name":"Ali Hassnain", "user_name":"ali", "password":"ali"})
    assert response.status_code == 400
    

