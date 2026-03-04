from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.profile import Profile
from app.services.tdee import calculate_tdee, protein_target

router = APIRouter(prefix="/profile", tags=["Profile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/setup")
def setup_profile(
    user_id: int,
    weight: float,
    height: float,
    age: int,
    gender: str,
    activity: str,
    goal: str,
    db: Session = Depends(get_db)
):

    tdee = calculate_tdee(weight, height, age, gender, activity)

    protein_day, protein_week = protein_target(weight, goal)

    profile = Profile(
        user_id=user_id,
        weight=weight,
        height=height,
        age=age,
        gender=gender,
        activity_level=activity,
        goal=goal,
        tdee=tdee,
        protein_per_day=protein_day,
        protein_per_week=protein_week
    )

    db.add(profile)
    db.commit()

    return {
        "tdee": tdee,
        "protein_day": protein_day,
        "protein_week": protein_week
    }