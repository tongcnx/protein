# database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///.test.db"

# ถ้าไม่มี env → ใช้ SQLite local
if not DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app/nutrition.db"

# Render ให้ postgres:// แต่ SQLAlchemy ต้อง postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://nutrition_user:84Zv89By90MpWjKv1hfXnjpXH5rT18Jo@dpg-d6dbfoktgctc73f1n400-a.singapore-postgres.render.com/nutrition_1t51", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
