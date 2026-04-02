from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from database import Users
from main import templates

from ..utils import dbDependency, getCurrentUser

homeRouter = APIRouter(prefix="/home")


@homeRouter.get("/")
async def home(request: Request, db: dbDependency):
    try:
        userData = await getCurrentUser(request)
        user = db.query(Users).filter(Users.id == userData.get("id")).first()
        if not user:
            return RedirectResponse(url="/auth/login")
        return templates.TemplateResponse(request, "home.html", context={"user": user})
    except HTTPException:
        return RedirectResponse(url="/auth/login")
