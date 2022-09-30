from typing import List, Optional
from fastapi import APIRouter,Depends,HTTPException,status,Response
from ..models import models
from ..schemas import schema
from ..config.db import get_db
from sqlalchemy.orm import Session
from .. import oauth2

post = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@post.get("/", response_model=List[schema.post.Post])
async def getPost(db: Session = Depends(get_db), user:int = Depends(oauth2.getCurrentUser),   limit:int = 10, skip:int = 0, search:Optional[str]=""):
    return db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

@post.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.post.Post)
async def createPost(post:schema.post.CreatePost, db: Session = Depends(get_db), user:int = Depends(oauth2.getCurrentUser)):  
    new_post = models.Posts(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@post.get("/latest", response_model=schema.post.Post)
async def getLatest(db: Session = Depends(get_db), user:int = Depends(oauth2.getCurrentUser)):  
    return db.query(models.Posts).order_by(models.Posts.id.desc()).first()

@post.get("/{id}", response_model=schema.post.Post)
async def getPostById(id:int, response: Response, db: Session = Depends(get_db), user:int = Depends(oauth2.getCurrentUser)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    return post 

@post.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePostById(id:int, db: Session = Depends(get_db), user:int = Depends(oauth2.getCurrentUser)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    if post.owner_id != user.owner_id:
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action"))
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@post.put("/{id}", response_model=schema.post.Post)
async def updatePost(id:int, post:schema.post.CreatePost, db: Session = Depends(get_db), user:int = Depends(oauth2.getCurrentUser)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    if post.owner_id != user.owner_id:
        raise(HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action"))
    new_post = models.Posts(**post.dict())
    db.query(models.Posts).filter(models.Posts.id == id).update(new_post,synchronize_session=False)
    db.commit()
    db.refresh(new_post)
    return new_post