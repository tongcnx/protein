from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import (
    auth,
    profile,
    dashboard,
    meal,
    shopping,
    budget,
    report,
    trainer
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(dashboard.router)
app.include_router(meal.router)
app.include_router(shopping.router)
app.include_router(budget.router)
app.include_router(report.router)
app.include_router(trainer.router)


@app.get("/")
def root():
    return {"status":"running"}