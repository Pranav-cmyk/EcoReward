from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request, Response, status

from database import Users
from main import templates

from ..utils import (
    createAccessToken,
    dbDependency,
    fetchAndAuthenticateUser,
    hashPassword,
)
from .models import UserModel, responseTokenModel

authRouter = APIRouter(prefix="/auth")


@authRouter.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse(request, "signup.html")


@authRouter.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(request, "login.html")


@authRouter.post("/createUser")
async def createUser(user: UserModel, db: dbDependency):
    if db.query(Users).filter(user.username == Users.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    new_user = Users(username=user.username, hashedPassword=hashPassword(user.password))
    db.add(new_user)
    db.commit()
    return {"status": "success", "username": user.username}


@authRouter.post("/token", response_model=responseTokenModel)
async def generateToken(user_data: UserModel, db: dbDependency, response: Response):
    user = fetchAndAuthenticateUser(user_data.username, user_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = createAccessToken(user.username, user.id, "user", timedelta(minutes=60))

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,
        samesite="lax",
    )

    return {"access_token": token, "token_type": "bearer"}
