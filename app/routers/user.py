from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from ..models.models import Users
from ..schemas import schema
from ..config.db import get_db
from .. import utils

user = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user.get("/")
async def getUsers(db: Session = Depends(get_db)):
    return db.query(Users).all()

@user.get("/{id}", response_model=schema.user.UserResponse)
async def getUserById(id:int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

@user.post("/", response_model=schema.user.UserResponse)
async def createUser(user:schema.user.UserBase, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user.put("/{id}")
async def updateUser(id:int, updated_user:schema.user.UserBase, db: Session = Depends(get_db)):
    user_query = db.query(Users).filter(Users.id == id)
    user = user_query.first()
    if user == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    
    user_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()

    return user_query.first()

@user.delete("/{id}")
async def deleteUser(id:int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id)
    if user.first() == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)