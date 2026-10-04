from fastapi import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import UserIn, UserSignUP, UserOut, Token
import bcrypt
import os
from dotenv import load_dotenv
from dependencies import get_db
from models import User
import jwt


router = APIRouter()
load_dotenv()

@router.post("/signup", response_model=UserOut)
def user_signup(user: UserSignUP, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(full_name=user.full_name, user_name=user.user_name, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    return new_user


@router.post("/login", response_model=Token)
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