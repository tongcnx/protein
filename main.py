from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.calculator import *
from core.food_engine import calculate_food_requirements, calculate_portfolio, load_foods

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
    foods = load_foods()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "food_analysis": foods
    })



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

@app.post("/portfolio")
async def portfolio(
    request: Request,
    weekly_protein: float = Form(...),
    chicken_percent: float = Form(0),
    egg_percent: float = Form(0),
    whey_percent: float = Form(0),
    fish_percent: float = Form(0),
    meals_per_day: int = Form(3)
):

    try:

        total_percent = chicken_percent + egg_percent + whey_percent + fish_percent

        if total_percent != 100:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": "เปอร์เซ็นต์รวมต้องเท่ากับ 100%"
            })

        foods = {
            "อกไก่ (100g โปรตีน 31g)": 31,
            "ไข่ (ฟองละ 6g)": 6,
            "เวย์ (1 scoop 24g)": 24,
            "ปลา (100g โปรตีน 22g)": 22
        }

        results = {}

        # คำนวณแต่ละตัว
        if chicken_percent > 0:
            protein = weekly_protein * (chicken_percent / 100)
            grams = protein / 31 * 100
            results["อกไก่"] = round(grams, 1)

        if egg_percent > 0:
            protein = weekly_protein * (egg_percent / 100)
            eggs = protein / 6
            results["ไข่ (ฟอง)"] = round(eggs, 1)

        if whey_percent > 0:
            protein = weekly_protein * (whey_percent / 100)
            scoops = protein / 24
            results["เวย์ (scoop)"] = round(scoops, 1)

        if fish_percent > 0:
            protein = weekly_protein * (fish_percent / 100)
            grams = protein / 22 * 100
            results["ปลา (กรัม)"] = round(grams, 1)

        daily_protein = weekly_protein / 7
        protein_per_meal = daily_protein / meals_per_day

        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": results,
            "daily_protein": round(daily_protein,1),
            "protein_per_meal": round(protein_per_meal,1)
        })

    except Exception as e:
        print("ERROR:", e)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "เกิดข้อผิดพลาดในระบบ กรุณาลองใหม่"
        })
