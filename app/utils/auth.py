from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from ..config import settings
from ..schemas.user_schemas import TokenData

# 
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Hash the password
def hash_password(password: str):
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)    

# Verify the password by comparing the actual and the hashed passwords
def verify_password(unhashed_password: str, hashed_password: str):
    return pwd_context.verify(unhashed_password, hashed_password)


# Create the acess token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt     

# Veify the token and get user id
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)
        return token_data
    
    except JWTError:
        raise credentials_exception
        