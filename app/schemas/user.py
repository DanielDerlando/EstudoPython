from datetime import datetime
from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):    
    email:EmailStr
    password:str