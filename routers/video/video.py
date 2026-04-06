import os
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from main import templates
from ..utils import getCurrentUser, dbDependency
from database import Users
from database.models import historyModel

from time import sleep
from google.genai import Client
from google.genai import types
from dotenv import load_dotenv
from .models import AnalysisResult
from .prompts import PROMPT

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
client = Client(api_key=api_key)
videoRouter = APIRouter(prefix="/video", tags=["video"])
MODEL = "gemini-3-flash-preview"


@videoRouter.get("/")
async def video(request: Request, db: dbDependency):
    try:
        userData = await getCurrentUser(request)
        user = db.query(Users).filter(Users.id == userData.get("id")).first()
        return templates.TemplateResponse(request, "video.html", context={"user": user})
    except HTTPException:
        return RedirectResponse(url="/auth/login")
    
@videoRouter.post("/upload")
async def uploadVideo(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(status_code=400, detail="Only MP4 files are allowed")
    print("Received video file" + file.filename)

    videoBytes = await file.read()
    print("Uploading to the geminiAPI")
    response = client.models.generate_content(
        model = MODEL,
        contents = [
            types.Part.from_bytes(
                data=videoBytes,
                mime_type=file.content_type
            ),
            types.Part.from_text(text=PROMPT)
        ],
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AnalysisResult
        )
    ).parsed

    return {"status": response.validVideo, 
            "filename": file.filename, 
            "result": response}
   
   
@videoRouter.post("/submit")
async def submitData(request: Request, db: dbDependency, history: historyModel):
    try:
        userData = await getCurrentUser(request)
        user = db.query(Users).filter(Users.id == userData.get("id")).first()

        # Update History (JSON list re-assignment to trigger SQLAlchemy update)
        updated_history = list(user.history)
        updated_history.append(history.model_dump()) 
        user.history = updated_history 

        # Update Points
        user.points += history.points
        user.currentPoints += history.points

        db.add(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success"}