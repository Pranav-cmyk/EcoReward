import os

from dotenv import load_dotenv

from database import SessionLocal, Users

load_dotenv()


"""
    Database connection utilities.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session


def databaseConnection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


dbDependency = Annotated[Session, Depends(databaseConnection)]


"""
    Password hashing and verification utilities.
"""

from passlib.context import CryptContext

bcryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password: str):
    return bcryptContext.hash(password)


def verifyPassword(password: str, hashed_password: str):
    return bcryptContext.verify(password, hashed_password)


"""
    User Auth & JWT token utilities.
"""

from jose import JWTError, jwt


def fetchAndAuthenticateUser(username: str, password: str, db) -> Users:
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not verifyPassword(password, user.hashedPassword):
        return False
    return user


def createAccessToken(username: str, userID: int, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": userID, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))


"""
    Decoding JWT tokens.
"""

from fastapi import Request, HTTPException, status

async def getCurrentUser(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        return {
            "username": payload.get("sub"),
            "id": payload.get("id"),
            "role": payload.get("role"),
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


userDependency = Annotated[dict, Depends(getCurrentUser)]
