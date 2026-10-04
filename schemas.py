from pydantic import BaseModel

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
