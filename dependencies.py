
from database import sessionlocal
from fastapi.security import HTTPBearer
from fastapi import Depends
from fastapi import HTTPException
import jwt
import os
from dotenv import load_dotenv


load_dotenv()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBearer()
def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    try:
        return jwt.decode(token, os.getenv("jwt_secret_key"), algorithms = ["HS256"])

    except jwt.InvalidTokenError as ite:
        print(f"The token is invalid or expired: {ite}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")