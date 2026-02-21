from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from auth import hash_password, verify_password, create_access_token
from database import Base
from jose import jwt
from fastapi.staticfiles import StaticFiles
from dependencies import get_current_user



import random

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse("index.html", {
        "request": request,
        "weight": "",
        "height": "",
        "age": "",
        "gender": "male",
        "activity": "1.2",
        "goal": "maintain"
    })



@app.post("/calculate", response_class=HTMLResponse)
def calculate(
    request: Request,
    user=Depends(get_current_user),
    weight: float = Form(...),
    height: float = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    activity: float = Form(...),
    goal: str = Form(...)
):

    # ===== BMR =====
    if gender == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    tdee = bmr * activity

    if goal == "gain":
        tdee += 300
    elif goal == "cut":
        tdee -= 300

    daily_protein = weight * 2
    weekly_protein = daily_protein * 7

    return templates.TemplateResponse("index.html", {
        "request": request,
        "weight": weight,
        "height": height,
        "age": age,
        "gender": gender,
        "activity": str(activity),
        "goal": goal,
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "daily_protein": round(daily_protein, 1),
        "weekly_protein": round(weekly_protein, 1)
    })


@app.post("/portfolio", response_class=HTMLResponse)
def portfolio(
    request: Request,
    user=Depends(get_current_user),
    weekly_protein: float = Form(...),
    meals_per_day: int = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    activity: str = Form(...),
    goal: str = Form(...),
    chicken_percent: float = Form(...),
    pork_percent: float = Form(...),
    beef_percent: float = Form(...),
    egg_percent: float = Form(...),
    fish_percent: float = Form(...),
    whey_percent: float = Form(...)
):

    activity_value = float(activity)

    # ===== BMR =====
    if gender == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    tdee = bmr * activity_value

    if goal == "gain":
        tdee += 300
    elif goal == "cut":
        tdee -= 300

    daily_protein = weekly_protein / 7
    protein_per_meal = daily_protein / meals_per_day

    total_percent = (
        chicken_percent + pork_percent + beef_percent +
        egg_percent + fish_percent + whey_percent
    )

    if total_percent != 100:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "เปอร์เซ็นต์รวมต้องเท่ากับ 100%",
            "weight": weight,
            "height": height,
            "age": age,
            "gender": gender,
            "activity": activity,
            "goal": goal,
            "bmr": round(bmr, 1),
            "tdee": round(tdee, 1),
            "daily_protein": round(daily_protein, 1),
            "weekly_protein": weekly_protein
        })

    protein_sources = {
        "เนื้อไก่": (21, chicken_percent),
        "เนื้อหมู": (22, pork_percent),
        "เนื้อวัว": (26, beef_percent),
        "เนื้อปลา": (22, fish_percent),
        "ไข่ไก่": (8, egg_percent),
        "เวย์": (80, whey_percent),
    }

    prices = {
        "เนื้อไก่": 100,
        "เนื้อหมู": 200,
        "เนื้อวัว": 280,
        "เนื้อปลา": 180,
        "ไข่ไก่": 140,
        "เวย์": 990,
    }

    results = {}
    chart_data = {}
    total_cost = 0

    for food, (protein_per_100g, percent) in protein_sources.items():

        protein_needed = weekly_protein * (percent / 100)
        grams_needed = (protein_needed / protein_per_100g) * 100
        kg_needed = grams_needed / 1000
        cost = kg_needed * prices[food]

        total_cost += cost
        results[food] = f"{round(grams_needed,1)} g (~{round(cost,0)} บาท)"
        chart_data[food] = round(grams_needed, 1)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "weight": weight,
        "height": height,
        "age": age,
        "gender": gender,
        "activity": activity,
        "goal": goal,
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "daily_protein": round(daily_protein, 1),
        "weekly_protein": weekly_protein,
        "protein_per_meal": round(protein_per_meal, 1),
        "results": results,
        "chart_data": chart_data,
        "total_cost": round(total_cost, 0)
    })

@app.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Passwords do not match"
        })

    user = db.query(User).filter(User.email == email).first()
    if user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Email already registered"
        })

    new_user = User(email=email, password=hash_password(password))
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)



@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid email or password"
        })

    access_token = create_access_token({"sub": user.email})

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=True  # Render ใช้ https
    )

    return response


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

