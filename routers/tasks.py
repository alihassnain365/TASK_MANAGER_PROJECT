from fastapi import APIRouter
from fastapi import HTTPException
from schemas import TaskOut, TaskCreate
from fastapi import Depends
from dependencies import get_db, verify_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Task

import services.tasks as services
import services.exceptions as exceptions
router = APIRouter()


"""1. create task"""
@router.post("/create/task", response_model=TaskOut, status_code=201)
def create_task(task_detail: TaskCreate, db: Session = Depends(get_db), current_user:dict = Depends(verify_token)):
    return services.create_task(db,task_detail.title,current_user["id"],status=False)

"""2. get task list of the user"""
@router.get("/tasks", response_model=list[TaskOut])
def get_tasks(db:Session= Depends(get_db), current_user:dict= Depends(verify_token)):
    try:
        return services.get_list(db,current_user["id"])
    except exceptions.TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")

"""3. mark task complete"""
@router.patch("/mark_task/{task_id}/complete", response_model=TaskOut)
def mark_task(task_id:int, db:Session=Depends(get_db), current_user:dict =Depends(verify_token)):
    try:
        return services.mark_task_complete(db,task_id,current_user["id"])
    except exceptions.ForbidenRequest:
        raise HTTPException(status_code=403, detail="Forbiden request")
    except exceptions.TaskNotFound:
        raise HTTPException(status_code=404, detail="Task Not found")

"""4. delete task"""
@router.delete("/delete_task/{task_id}", status_code=204)
def delete_task(task_id:int, db:Session=Depends(get_db), current_user:dict=Depends(verify_token)):
    try:
        services.delete_task(db,task_id,current_user["id"])
    except exceptions.TaskNotFound:
        raise HTTPException(status_code=404, detail="Task Not found")
    except exceptions.ForbidenRequest:
        raise HTTPException(status_code=403, detail="Forbiden request")


