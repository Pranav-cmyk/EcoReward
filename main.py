from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="./templates")

from routers import authRouter, homeRouter

app.include_router(authRouter)
app.include_router(homeRouter)


@app.get("/")
async def root():
    return RedirectResponse(url="/home/")
