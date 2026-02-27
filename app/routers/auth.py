from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(
    name:str,
    email:str,
    password:str,
    db:Session = Depends(get_db)
):

    exist = db.query(User).filter(
        User.email == email
    ).first()

    if exist:
        raise HTTPException(400,"email exists")

    user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()

    return {"message":"user created"}



@router.post("/login")
def login(
    email:str,
    password:str,
    db:Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email==email
    ).first()

    if not user:
        raise HTTPException(401,"invalid email")

    if not verify_password(password,user.password):
        raise HTTPException(401,"wrong password")

    token = create_access_token(
        {"user_id":user.id}
    )

    return {
        "access_token":token,
        "token_type":"bearer"
    }