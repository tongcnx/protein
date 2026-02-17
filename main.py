from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.calculator import *
from core.food_engine import calculate_food_requirements

app = FastAPI()
templates = Jinja2Templates(directory="templates")


activity_map = {
    "1.2": 1.2,
    "1.375": 1.375,
    "1.55": 1.55,
    "1.725": 1.725
}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/calculate", response_class=HTMLResponse)
def calculate(
    request: Request,
    weight: float = Form(...),
    height: float = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    activity: str = Form(...),
    goal: str = Form(...)
):
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_map[activity])
    daily_protein, weekly_protein = calculate_protein(weight, goal)

    food_analysis = calculate_food_requirements(weekly_protein)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "daily_protein": round(daily_protein, 2),
        "weekly_protein": round(weekly_protein, 2),
        "food_analysis": food_analysis
    })
