from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, Base

# Models
from app.models.user import User
from app.models.protein_source import ProteinSource
from app.models.allergy import UserAllergy
from app.models.portfolio import ProteinPortfolio
from app.models.menu import Menu
from app.models.weekplan import WeekPlan

app = FastAPI(
    title="Protein Planner API",
    version="1.0"
)


# -------------------------
# AUTO CREATE DATABASE
# -------------------------

@app.on_event("startup")
def startup():

    print("Creating tables...")

    Base.metadata.create_all(bind=engine)

    print("Tables Ready")


# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/")
def root():
    return {"status": "running"}


# -------------------------
# INSERT DEFAULT PROTEIN
# -------------------------

@app.on_event("startup")
def insert_protein_sources():

    with engine.connect() as conn:

        result = conn.execute(text(
            "SELECT COUNT(*) FROM protein_sources"
        ))

        count = result.scalar()

        if count == 0:

            print("Insert default proteins...")

            conn.execute(text("""

            INSERT INTO protein_sources
            (name, protein_per_100g, price_per_kg, category)
            VALUES

            ('Chicken Breast',31,120,'meat'),
            ('Pork',27,140,'meat'),
            ('Beef',26,250,'meat'),
            ('Salmon',25,400,'fish'),
            ('Egg',13,80,'egg'),
            ('Tofu',10,60,'plant'),
            ('Whey Protein',80,900,'supplement')

            """))

            conn.commit()

            print("Protein inserted")


# -------------------------
# ROUTERS
# -------------------------

from app.routers import auth
from app.routers import protein
from app.routers import portfolio
from app.routers import menu
from app.routers import shopping

app.include_router(auth.router)
app.include_router(protein.router)
app.include_router(portfolio.router)
app.include_router(menu.router)
app.include_router(shopping.router)