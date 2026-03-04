from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.database import Base, engine
from app.routers import protein_engine

from app.routers import (
    auth,
    profile,
    protein,
    meal,
    shopping
)

app = FastAPI()

# Create tables
@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)


# Routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(protein.router)
app.include_router(meal.router)
app.include_router(shopping.router)
app.include_router(protein_engine.router)


# Static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def root():
    return {"app":"Protein Planner API"}