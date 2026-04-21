from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner: UserOut

    model_config = {"from_attributes": True}

class Out(BaseModel):
    Post : PostOut
    vote : int
    model_config = {"from_attributes": True}

class PostResponse(BaseModel):
    Post : PostOut
    vote : int

    class config : 
        orm_mode = True

class Token(BaseModel):
    access_token : str
    token_type : str
class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir : conint(le = 1)  # type: ignore