from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.protein import ProteinRecord
from app.dependencies import get_current_user

router = APIRouter(prefix="/protein")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_protein(
    protein: float,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    record = ProteinRecord(
        protein=protein,
        user_id=user.id
    )

    db.add(record)
    db.commit()

    return {"status": "added"}


@router.get("/my")
def my_protein(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    records = db.query(ProteinRecord).filter(
        ProteinRecord.user_id == user.id
    ).all()

    return records