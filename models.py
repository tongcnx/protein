from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    weekly_records = relationship("WeeklyRecord", back_populates="user")


class WeeklyRecord(Base):
    __tablename__ = "weekly_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    week_label = Column(String)
    weight = Column(Float)
    weekly_protein = Column(Float)
    total_cost = Column(Float)
    actual_cost = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="weekly_records")
