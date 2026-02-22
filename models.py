from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
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

class MealPlan(Base):
    __tablename__ = "mealplans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    calorie_target = Column(Float)
    protein_target = Column(Float)
    total_calories = Column(Float)
    total_protein = Column(Float)
    total_cost = Column(Float)
    protein_split = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("MealItem", back_populates="mealplan")


class MealItem(Base):
    __tablename__ = "mealitems"

    id = Column(Integer, primary_key=True, index=True)
    mealplan_id = Column(Integer, ForeignKey("mealplans.id"))
    food_name = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    cost = Column(Float)

    mealplan = relationship("MealPlan", back_populates="items")