from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from main import templates
from ..utils import getCurrentUser, dbDependency
from database import Users

videoRouter = APIRouter(prefix="/video", tags=["video"])

@videoRouter.get("/")
async def video(request: Request, db: dbDependency):
    try:
        userData = await getCurrentUser(request)
        user = db.query(Users).filter(Users.id == userData.get("id")).first()
        return templates.TemplateResponse(request, "video.html", context={"user": user})
    except HTTPException:
        return RedirectResponse(url="/auth/login")