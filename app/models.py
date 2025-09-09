from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Book(BaseModel):
    title: str
    author: str
    genre: Optional[str]
    status: str = Field(default="to-read", pattern="^(to-read|reading|finished)$")

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    status: Optional[str]

class User(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class BookOut(BaseModel):
    id: str
    title: str
    author: str
    genre: Optional[str] = None
