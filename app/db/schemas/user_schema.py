from pydantic import BaseModel
from typing import Optional

# User related schemas
class UserBase(BaseModel):
    email: str
    username: str
    nickname: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    id: str
    password: str
