

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

SECRET_KEY = "super_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Auth(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    password: str

db_user = []


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/login")
def login(auth: Auth):

    for user in db_user:
        if user.username == auth.username and user.password == auth.password:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            return create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    raise HTTPException(status_code=400, detail= "User not found")

@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int, token: str):
    decoded = jwt.decode(token, SECRET_KEY)

    return decoded


@app.post("/user", response_model=User)
def create_user(user: User):
    db_user.append(user)
    return user