from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from models import User, Task
from sqlalchemy.orm import Session
from database import sessionlocal
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import select
import bcrypt
import os
import jwt


app = FastAPI()
load_dotenv()
security = HTTPBearer()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


class UserOut(BaseModel):
    id: int
    full_name: str
    user_name: str

class UserIn(BaseModel):
    user_name: str
    password: str

class UserSignUP(BaseModel):
    full_name: str
    user_name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title:str

class TaskOut(BaseModel):
    id: int
    title: str
    status: bool


""" verifying the jwt token """
def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    try:
        return jwt.decode(token, os.getenv("jwt_secret_key"), algorithms = ["HS256"])

    except jwt.InvalidTokenError as ite:
        print(f"The token is invalid or expired: {ite}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


"""1. User Sign UP"""

@app.post("/signup", response_model=UserOut)
def user_signup(user: UserSignUP, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(full_name=user.full_name, user_name=user.user_name, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    return new_user

"""2. User Log In"""
@app.post("/login", response_model=Token)
def user_login(user:UserIn, db:Session = Depends(get_db)):
    req_user = db.execute(select(User).where(User.user_name == user.user_name)).scalar_one_or_none()
    if req_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if bcrypt.checkpw(user.password.encode('utf-8'),req_user.hashed_password.encode('utf-8')):
        payload = {
            "id": req_user.id,
            "user_name": user.user_name
        }
        token = jwt.encode(payload, os.getenv("jwt_secret_key"),algorithm="HS256")

        return {
            "access_token": token, 
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

@app.post("/create/task", response_model=TaskOut, status_code=201)
def create_task(task_detail: TaskCreate, db: Session = Depends(get_db), current_user:dict = Depends(verify_token)):
    new_task = Task(title= task_detail.title, status= False, user_id = current_user["id"])
    db.add(new_task)
    db.commit()
    return new_task

@app.get("/tasks", response_model=list[TaskOut])
def get_tasks(db:Session= Depends(get_db), current_user:dict= Depends(verify_token)):
    user = current_user["id"]
    task_list = db.execute(select(Task).where(Task.user_id == user)).scalars().all()
    return task_list

@app.patch("/mark_task/{task_id}/complete", response_model=TaskOut)
def mark_task(task_id:int, db:Session=Depends(get_db), current_user:dict =Depends(verify_token)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task doesn't exists")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code = 403, detail="You can't access")
    task.status = True
    db.commit()
    return task

@app.delete("/delete_task/{task_id}", status_code=204)
def delete_task(task_id:int, db:Session=Depends(get_db), current_user:dict=Depends(verify_token)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not exist")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You are not allowed")
    db.delete(task)
    db.commit()

