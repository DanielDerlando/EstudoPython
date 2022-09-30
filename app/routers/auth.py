from fastapi import APIRouter,Depends,HTTPException,status,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..config.db import get_db
from ..schemas import schema
from ..models.models import Users
from .. import utils,oauth2


auth = APIRouter(
    tags=["Authentication"]
)

@auth.post("/login", response_model=schema.oauth2.Token)
async def getToken(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    hashed_password = user.password

    if not utils.verifyHash(user_credentials.password,hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    jwt_token = oauth2.createAccessToken(data={"user_id":user.id})

    return {"access_token":jwt_token, "token_type":"bearer"}