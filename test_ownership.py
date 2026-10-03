"""in this file we will test that the relevant user can change the relevant tasks"""
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)

def get_token(username:str, password:str):
    response = client.post("/login", json={"user_name":username, "password":password})
    return response.json()["access_token"]

def test_ali_cannot_access_shami_task():
    # shami logged in and created the task, whit shami_task_id
    shami_token = get_token("shami","shami")
    create_task = client.post("/create/task", json={"title":"pray isha"}, headers={"Authorization": f"Bearer {shami_token}"})
    shami_task_id = create_task.json()["id"]

    # now ali is logged in and he would try to access shami_task_id
    ali_token = get_token("ali","ali")
    response = client.patch(f"/mark_task/{shami_task_id}/complete", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 403 # i know who you are , but you are not allowed to do that


def test_ali_can_complete_his_task():
    ali_token = get_token("ali","ali")
    # ali is creating a task
    ali_task = client.post("/create/task", json={"title":"pray fajr"}, headers={"Authorization": f"Bearer {ali_token}"})
    ali_task_id = ali_task.json()["id"]

    # now ali is marking complete to his task
    response = client.patch(f"/mark_task/{ali_task_id}/complete", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 200
    assert response.json()["status"] == True
    
def test_ali_cannot_delete_shami_task():
    # shami login and create a task
    shami_token = get_token("shami","shami")
    shami_task = client.post("/create/task", json={"title":"pray five times a day"}, headers={"Authorization": f"Bearer {shami_token}"})
    shami_task_id = shami_task.json()["id"]

    # ali login and try to delete the shami's task
    ali_token = get_token("ali","ali")
    response = client.delete(f"/delete_task/{shami_task_id}", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 403 # i know you who you are but you are not allowed to do this

def test_ali_can_delete_his_own_task():
    # ali login and creates a task
    ali_token = get_token("ali","ali")
    ali_task = client.post("/create/task", json={"title":"do hardwork, allah will help you"}, headers={"Authorization": f"Bearer {ali_token}"})
    ali_task_id = ali_task.json()["id"]

    # now ali deletes his task
    response = client.delete(f"/delete_task/{ali_task_id}", headers={"Authorization": f"Bearer {ali_token}"})
    assert response.status_code == 204 # no return content
