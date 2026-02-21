from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("postgresql://nutrition_user:n4h0O5qx27fnovgyIjfxsDQl1RNKCQt1@dpg-d6clvr7fte5s73cs5s3g-a/nutrition_p23w")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

