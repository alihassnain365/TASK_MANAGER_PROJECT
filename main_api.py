from fastapi import FastAPI
from routers import auth, tasks
from dependencies import get_db


app = FastAPI()
app.include_router(auth.router)
app.include_router(tasks.router)











