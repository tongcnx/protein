from fastapi import APIRouter

router = APIRouter(prefix="/report", tags=["report"])

@router.get("/")
def report_home():
    return {"report": "ok"}