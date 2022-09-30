from msilib import schema
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError,jwt
from datetime import datetime,timedelta
from .schemas import schema
from .models.models import Users
from .config.db import get_db
from .config.config import settings

#random text, for ex a random hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def createAccessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verifyAccessToken(token:str, credentials_exceptions):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data = schema.oauth2.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions

    return token_data    

def getCurrentUser(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validated credentials",headers={"WWW-Authenticate": "Bearer"})
    token = verifyAccessToken(token,credentials_exceptions)
    user = db.query(Users).filter(Users.id==token.id).first()
    return user