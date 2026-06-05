from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from .user_schemas import FetchUser
from pydantic.types import conint

"""ARTICLE SCHEMAS"""
# Article base class
class BaseArticle(BaseModel):
    title: str
    content: str

# Inherits from base article
class CreateArticle(BaseArticle):
    pass

class UpdateArticle(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class ArticleResponse(BaseArticle):
    id: int
    published_at: datetime
    user_id: int
    user: FetchUser
    
    model_config = ConfigDict(
        from_attributes=True, 
        extra='forbid',
        json_encoders={
        datetime: lambda v: v.isoformat()})