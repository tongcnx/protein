from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user import User

SECRET_KEY="SUPER_SECRET_KEY_12345"
ALGORITHM="HS256"


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token:str,
    db:Session=Depends(get_db)
):

    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id=payload.get("user_id")

    except JWTError:
        raise HTTPException(401,"invalid token")

    user=db.query(User).get(user_id)

    return user