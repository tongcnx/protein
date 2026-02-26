# app/routers/profile.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db

router = APIRouter()

@router.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    # ตัวอย่าง query
    # user = db.query(User).first()
    return {"message": "Profile page working"}
