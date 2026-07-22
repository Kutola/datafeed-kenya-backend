from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import models
from ..schemas import user_schemas
from ..utils.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Register endpoint
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: user_schemas.CreateUser, db: Session = Depends(get_db)):
    # Normalize user to lowercase
    user_dict = user.model_dump()
    user_dict['name'] = user_dict['name'].lower().strip()

    # Check if user already exists
    existing_user = db.query(models.User).filter(
        func.lower(models.User.name) == user_dict['name']
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = hash_password(user.password)

    # Create a new user object
    new_user = models.User(
        name=user.name,
        role=user.role,
        email=user.email,
        password=hashed_password,
        phone=user.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=user_schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Convert input username to lowercase
    username = user_credentials.username.lower().strip()
    
    # check if the user exists
    user = db.query(models.User).filter(
        func.lower(models.User.email) == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    # Verify password
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    # Create JWT token
    access_token = create_access_token(data={"user_id": user.id})
    return{
        "access_token": access_token,
        "token_type": "bearer"
    }