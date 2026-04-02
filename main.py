from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="./templates")

from routers import authRouter

app.include_router(authRouter)


@app.get("/")
async def root():
    return RedirectResponse(url="/auth/signup")
