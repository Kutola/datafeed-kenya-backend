from fastapi import FastAPI, Response, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from ..schemas import article_schemas
from ..models import models
from ..database import get_db
from .users import get_user
from ..dependencies import oauth2

router = APIRouter(
    prefix="/articles",
    tags=['Articles']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=article_schemas.ArticleResponse )
def create_article(article: article_schemas.CreateArticle, db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user)):
    
    new_article = models.Article(user_id=current_user.id, **article.model_dump())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article

@router.get("/", response_model=List[article_schemas.ArticleResponse])
def get_articles(db: Session = Depends(get_db)): 
    articles = db.query(models.Article).all()
    return articles

@router.get("/{id}", response_model=article_schemas.ArticleResponse)
def get_article(id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == id).first()
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id: {id} doesn't exist"
        )    
    return article


@router.put("/{id}", response_model=article_schemas.ArticleResponse)
def update_article(id: int, updated_article: article_schemas.CreateArticle, 
                   db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(models.Article.id == id).first()

    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Article with id: {id} doesn't exist")
    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to update the article'
        )
    
    # Update the fields
    article_dict = updated_article.model_dump(exclude_unset=True)
    for key, value in article_dict.items():
        setattr(article, key, value)    
    
    # Execute and refresh to get the updated data
    db.commit()
    db.refresh(article)
    return article

    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    article = db.query(models.Article).filter(models.Article.id == id).first()

    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Article with id: {id} doesn't exist")
    if article.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You cannot delete this article")
    
    db.delete(article)
    db.commit()
    return
