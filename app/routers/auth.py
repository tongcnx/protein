from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.database.database import Base
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):

    user = User(
        name=name,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"status": "created"}