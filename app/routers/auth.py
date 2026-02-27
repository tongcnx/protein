from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(name:str,email:str,password:str,db:Session=Depends(get_db)):

    user = User(
        name=name,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()

    return {"message":"user created"}