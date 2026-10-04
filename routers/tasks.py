from fastapi import APIRouter
from fastapi import HTTPException
from schemas import TaskOut, TaskCreate
from fastapi import Depends
from dependencies import get_db, verify_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Task
router = APIRouter()


"""1. create task"""
@router.post("/create/task", response_model=TaskOut, status_code=201)
def create_task(task_detail: TaskCreate, db: Session = Depends(get_db), current_user:dict = Depends(verify_token)):
    new_task = Task(title= task_detail.title, status= False, user_id = current_user["id"])
    db.add(new_task)
    db.commit()
    return new_task

"""2. get task list of the user"""
@router.get("/tasks", response_model=list[TaskOut])
def get_tasks(db:Session= Depends(get_db), current_user:dict= Depends(verify_token)):
    user = current_user["id"]
    task_list = db.execute(select(Task).where(Task.user_id == user)).scalars().all()
    return task_list

"""3. mark task complete"""
@router.patch("/mark_task/{task_id}/complete", response_model=TaskOut)
def mark_task(task_id:int, db:Session=Depends(get_db), current_user:dict =Depends(verify_token)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task doesn't exists")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code = 403, detail="You can't access")
    task.status = True
    db.commit()
    return task

"""4. delete task"""
@router.delete("/delete_task/{task_id}", status_code=204)
def delete_task(task_id:int, db:Session=Depends(get_db), current_user:dict=Depends(verify_token)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not exist")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You are not allowed")
    db.delete(task)
    db.commit()

