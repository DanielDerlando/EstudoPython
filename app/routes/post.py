from fastapi import APIRouter,Depends,HTTPException,status,Response
from ..models.index import Posts
from ..schemas.index import Post
from ..config.db import get_db
from sqlalchemy.orm import Session

post = APIRouter()

@post.get("/")
async def getPost(db: Session = Depends(get_db)):
    return db.query(Posts).all()

@post.post("/", status_code=status.HTTP_201_CREATED)
async def createPost(post:Post, db: Session = Depends(get_db)):  
    new_post = Posts(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@post.get("/latest")
async def getLatest(db: Session = Depends(get_db)):  
    return db.query(Posts).order_by(Posts.id.desc()).first()

@post.get("/{id}")
async def getPostById(id:int, response: Response, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == id).first()
    if not post:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    return post 

@post.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePostById(id:int, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == id)
    if post.first() == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@post.put("/{id}")
async def updatePost(id:int, post:Post, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == id).first()
    if post == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    new_post = Posts(**post.dict())
    db.query(Posts).filter(Posts.id == id).update(new_post,synchronize_session=False)
    db.commit()
    db.refresh(new_post)
    return new_post