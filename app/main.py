from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{
        "title": "Olá Mundo",
        "content": "Teste",
        "published": True,
        "rating": None,
        "id": 1
    }]

def find_post(id:int):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id:int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
async def home():
    return {"Application is running"}

@app.get("/posts")
async def getPost():
    return my_posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def createPost(post:Post):  
    my_dict=post.dict()
    my_dict['id'] = randrange(0,100000000)
    my_posts.append(my_dict)
    return {"message": "created" }

@app.get("/posts/latest")
async def getLatest():  
    return my_posts[len(my_posts)-1]

@app.get("/posts/{id}")
async def getPostById(id:int, response: Response):
    post = find_post(id)
    if not post:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    return post 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def getPostById(id:int):
    index = find_index_post(id)
    if index == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def updatePost(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise(HTTPException(status.HTTP_404_NOT_FOUND))
    my_post = post.dict()
    my_post['id']=id
    my_posts[index]=my_post
    return my_post