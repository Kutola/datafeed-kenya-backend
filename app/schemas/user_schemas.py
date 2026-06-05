from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class BaseUser(BaseModel):
    name: str
    role: str
    email: EmailStr
    password: str
    phone: str

class CreateUser(BaseUser):
    pass

class UpdateUser(BaseUser):
    pass

class FetchUser(BaseModel):
    name: str
    role: str
    email: str
    phone: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None            