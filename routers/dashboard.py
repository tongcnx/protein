# app/routers/dashboard.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    return {"message": "Dashboard working"}
