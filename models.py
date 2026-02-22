from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DateTime

created_at = Column(DateTime, default=datetime.utcnow)

class WeeklyRecord(Base):
    __tablename__ = "weekly_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    week_label = Column(String)
    weight = Column(Float)
    weekly_protein = Column(Float)
    total_cost = Column(Float)
        created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
