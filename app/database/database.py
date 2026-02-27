import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_bass

DATABASE_URL = os.getenv("postgresql://nutrition_user:84Zv89By90MpWjKv1hfXnjpXH5rT18Jo@dpg-d6dbfoktgctc73f1n400-a.singapore-postgres.render.com/nutrition_1t51")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()