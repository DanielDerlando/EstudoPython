from typing import List
from fastapi import APIRouter,Depends,HTTPException,status,Response
from ..models import models
from ..schemas import schema
from ..config.db import get_db
from sqlalchemy.orm import Session

post = APIRouter()

@post.get("/", response_model=List[schema.post.Post])
async def getPost(db: Session = Depends(get_db)):
    return db.query(models.Posts).all()

@post.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.post.Post)
async def createPost(post:schema.post.CreatePost, db: Session = Depends(get_db)):  
    new_post = models.Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@post.get("/latest", response_model=schema.post.Post)
async def getLatest(db: Session = Depends(get_db)):  
    return db.query(models.Posts).order_by(models.Posts.id.desc()).first()

@post.get("/{id}", response_model=schema.post.Post)
async def getPostById(id:int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    return post 

@post.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePostById(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    if post.first() == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@post.put("/{id}", response_model=schema.post.Post)
async def updatePost(id:int, post:schema.post.CreatePost, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    new_post = models.Posts(**post.dict())
    db.query(models.Posts).filter(models.Posts.id == id).update(new_post,synchronize_session=False)
    db.commit()
    db.refresh(new_post)
    return new_post