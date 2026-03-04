# app/routers/auth.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
def login_page():
    return {"message": "Login page working"}
