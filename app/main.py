from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.database import Base, engine
from app.models.user import User
from sqlalchemy import text
from app.routers import protein
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
from app.routers.auth import router as auth_router


app = FastAPI()

@app.on_event("startup")
def startup():

    # ลบทุก table แบบ CASCADE
    with engine.connect() as conn:
        conn.execute(text("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        """))
        conn.commit()

    # สร้างใหม่ทั้งหมด
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(protein.router)

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

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"status":"running"}