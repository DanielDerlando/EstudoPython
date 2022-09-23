from fastapi import APIRouter,Depends,HTTPException,status,Response
from ..models.index import Users
from ..schemas.index import User
from ..config.db import get_db
from sqlalchemy.orm import Session

user = APIRouter()

@user.get("/")
async def getUsers(db: Session = Depends(get_db)):
    return db.query(Users).all()

@user.get("/{id}")
async def getUserById(id:int, db: Session = Depends(get_db)):
    return db.query(Users).filter(Users.id == id).first()

@user.post("/")
async def createUser(user:User, db: Session = Depends(get_db)):
    new_user = Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user.put("/{id}")
async def updateUser(id:int, updated_user:User, db: Session = Depends(get_db)):
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