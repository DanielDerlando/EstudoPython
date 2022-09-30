from datetime import datetime
from pydantic import BaseModel
from . import user

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class Post (PostBase):
    id: int
    create_at: datetime
    owner_id: int
    owner: user.UserResponse     
    class Config:
        orm_mode = True