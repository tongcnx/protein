from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user import User

from jose import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth")

SECRET_KEY = "MYSECRET123"
ALGORITHM = "HS256"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):

    user = User(
        name=name,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()

    return {"status": "created"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.password != password:
        raise HTTPException(status_code=401, detail="Wrong password")

    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=7)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "token": token
    }