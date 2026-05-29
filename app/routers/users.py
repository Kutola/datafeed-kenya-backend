from fastapi import FastAPI, Response, Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from ..schemas import user_schemas
from ..models import models
from ..database import get_db
from ..utils import auth
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schemas.FetchUser)
def create_user(user: user_schemas.CreateUser, db: Session = Depends(get_db)):
    
    # Hash user password before adding to db
    hashed_password = auth.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User credentials already exists"
        )

    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[user_schemas.FetchUser])
def get_users(db: Session = Depends(get_db)): 
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=user_schemas.FetchUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist"
        )    
    return user


@router.put("/{id}", response_model=user_schemas.FetchUser)
def update_user(id: int, updated_user: user_schemas.CreateUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models. User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} doesn't exist")
    
    
    # Update the fields
    user_dict = updated_user.model_dump(exclude_unset=True)
    for key, value in user_dict.items():
        setattr(user, key, value)    
    
    # Execute and refresh to get the updated data
    db.commit()
    db.refresh(user)
    return user

    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} doesn't exist")
    
    db.delete(user)
    db.commit()
    return
