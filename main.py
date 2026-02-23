from fastapi import FastAPI, Request, Form, Depends, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
from models import User, WeeklyRecord, MealPlan, MealItem
from auth import hash_password, verify_password, create_access_token
from database import Base
from jose import jwt
from fastapi.staticfiles import StaticFiles
from dependencies import get_current_user
from core.food_engine import generate_optimized_menu, load_foods
from core.god_engine import generate_week_plan
from collections import defaultdict


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

def generate_grocery_summary(mealplan):

    summary = defaultdict(lambda: {"amount": 0, "unit": ""})

    for item in mealplan.items:
        summary[item.food_name]["amount"] += item.amount
        summary[item.food_name]["unit"] = item.unit

    return summary

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user=Depends(get_current_user)
):
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
            "results": results,
            "protein_per_meal": protein_per_meal,
            "total_cost": total_cost,
            "weekly_protein": weekly_protein,
            "daily_protein": daily_protein,
            "tdee": tdee,
            "protein_split": {
                "chicken": chicken_percent,
                "pork": pork_percent,
                "beef": beef_percent,
                "egg": egg_percent,
                "fish": fish_percent,
                "whey": whey_percent,
            }
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

    # ===== SAVE WEEKLY RECORD =====
    from datetime import datetime

    db = SessionLocal()
    user_obj = db.query(User).filter(User.email == user).first()

    # สร้าง week label จากวันที่จริง
    week_label = datetime.utcnow().strftime("%Y-%m-%d")

    new_record = WeeklyRecord(
        user_id=user_obj.id,
        week_label=week_label,
        weight=weight,
        weekly_protein=weekly_protein,
        total_cost=total_cost
    )

    db.add(new_record)
    db.commit()
    db.close()

    # ===== RETURN TEMPLATE =====

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
        "total_cost": round(total_cost, 0),
        
        # ✅ ต้องมีอันนี้
            "protein_split": {
                "chicken": chicken_percent,
                "pork": pork_percent,
                "beef": beef_percent,
                "egg": egg_percent,
                "fish": fish_percent,
                "whey": whey_percent,
            }
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

    response = templates.TemplateResponse("login_success.html", {
        "request": request
    })

    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True
    )

    return response



@app.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    token: str | None = Cookie(default=None)
):
    if token:
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def root(request: Request, token: str | None = Cookie(default=None)):

    if not token:
        return RedirectResponse("/login", status_code=303)

    return RedirectResponse("/dashboard", status_code=303)

@app.get("/progress", response_class=HTMLResponse)
def progress(request: Request, user=Depends(get_current_user)):

    db = SessionLocal()
    user_obj = db.query(User).filter(User.email == user).first()

    records = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == user_obj.id
    ).order_by(WeeklyRecord.created_at).all()

    db.close()

    labels = [r.created_at.strftime("%d %b") for r in records]
    estimated = [round(r.total_cost, 2) for r in records]
    actual = [
        round(r.actual_cost, 2) if r.actual_cost else None
        for r in records
    ]

    return templates.TemplateResponse("progress.html", {
        "request": request,
        "records": records,
        "labels": labels,
        "estimated": estimated,
        "actual": actual
    })



@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("token")
    return response

@app.post("/update-actual")
def update_actual(
    record_id: int = Form(...),
    actual_cost: float = Form(...),
    user=Depends(get_current_user)
):

    db = SessionLocal()

    record = db.query(WeeklyRecord).filter(
        WeeklyRecord.id == record_id
    ).first()

    record.actual_cost = actual_cost

    db.commit()
    db.close()

    return RedirectResponse("/progress", status_code=303)


@app.get("/profile", response_class=HTMLResponse)
def profile(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # <-- รับเป็น email
):

    user_obj = db.query(User).filter(User.email == user).first()

    # ===== Weekly Records =====
    records = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == user_obj.id
    ).all()

    total_weeks = len(records)
    total_estimated = sum(r.total_cost for r in records)
    total_actual = sum(r.actual_cost for r in records if r.actual_cost)

    avg_estimated = total_estimated / total_weeks if total_weeks else 0
    avg_actual = total_actual / total_weeks if total_weeks else 0

    # ===== Meal Plans =====
    plans = db.query(MealPlan).filter(
        MealPlan.user_id == user_obj.id
    ).order_by(MealPlan.created_at.desc()).all()

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user_obj,
        "total_weeks": total_weeks,
        "avg_estimated": round(avg_estimated, 2),
        "avg_actual": round(avg_actual, 2),
        "plans": plans
    })



@app.get("/menu-generator", response_class=HTMLResponse)
def menu_generator(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "menu.html",
        {"request": request}
    )

@app.post("/generate-menu")
def generate_menu(
    request: Request,
    calorie_target: float = Form(...),
    protein_target: float = Form(...),
    budget: float = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = generate_optimized_menu(calorie_target, protein_target, budget)

    mealplan = MealPlan(
        user_id=current_user.id,   # ✅ ใช้ object ตรง ๆ
        calorie_target=calorie_target,
        protein_target=protein_target,
        total_calories=result["total_cal"],
        total_protein=result["total_protein"],
        total_cost=result["total_cost"],
    )

    db.add(mealplan)
    db.commit()
    db.refresh(mealplan)

    for item in result["menu"]:
        db_item = MealItem(
            mealplan_id=mealplan.id,
            food_name=item["name"],
            amount=item.get("amount", 1),
            unit=item.get("unit", "unit"),
            calories=item["calories"],
            protein=item["protein"],
            cost=item["price"],
        )
        db.add(db_item)

    db.commit()

    return templates.TemplateResponse(
        "menu.html",
        {
            "request": request,
            "result": result
        }
    )



@app.get("/meal-history", response_class=HTMLResponse)
def meal_history(request: Request, user=Depends(get_current_user)):

    db = SessionLocal()
    user_obj = db.query(User).filter(User.email == user).first()

    plans = db.query(MealPlan).filter(
        MealPlan.user_id == user_obj.id
    ).order_by(MealPlan.created_at.desc()).all()

    db.close()

    return templates.TemplateResponse(
        "meal_history.html",
        {"request": request, "plans": plans}
    )


@app.post("/generate-god-mode")
def generate_god_mode(
    request: Request,
    calorie_target: float = Form(...),
    protein_target: float = Form(...),
    budget: float = Form(None),
):

    from core.food_engine import load_foods
    from core.god_engine import generate_week_plan
    from core.meal_suggester import suggest_meals

    foods_dict = load_foods()

    foods = [
        {
            "name": name,
            "protein": data["protein"],
            "calories": data["calories"],
            "price": data["price"]
        }
        for name, data in foods_dict.items()
    ]

    week = generate_week_plan(
        foods,
        calorie_target,
        protein_target,
        None,   # no protein split here
        budget
    )

    # ✅ เพิ่ม Smart Suggestion
    for day in week:
        day["suggested_meals"] = suggest_meals(day)

    return templates.TemplateResponse(
        "menu.html",
        {
            "request": request,
            "week": week
        }
    )



@app.get("/grocery/{plan_id}")
def grocery_page(plan_id: int, request: Request):

    db = SessionLocal()
    mealplan = db.query(MealPlan).filter(MealPlan.id == plan_id).first()

    summary = generate_grocery_summary(mealplan)

    db.close()

    return templates.TemplateResponse(
        "grocery.html",
        {
            "request": request,
            "summary": summary,
            "mealplan": mealplan
        }
    )


@app.post("/save-week-plan")
def save_week_plan(
    calorie_target: float,
    protein_target: float,
    total_calories: float,
    total_protein: float,
    total_cost: float,
    protein_split: dict,
    menu: list,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    mealplan = MealPlan(
        user_id=current_user.id,
        calorie_target=calorie_target,
        protein_target=protein_target,
        total_calories=round(total_calories, 2),
        total_protein=round(total_protein, 2),
        total_cost=round(total_cost, 2),
        protein_split=protein_split
    )

    db.add(mealplan)
    db.commit()
    db.refresh(mealplan)

    # save items
    for item in menu:
        meal_item = MealItem(
            mealplan_id=mealplan.id,
            food_name=item["name"],
            amount=item.get("amount", 1),
            unit=item.get("unit", "g"),
            calories=round(item["calories"], 2),
            protein=round(item["protein"], 2),
            cost=round(item["cost"], 2)
        )
        db.add(meal_item)

    db.commit()

    return {"status": "saved"}


@app.post("/generate-from-portfolio")
def generate_from_portfolio(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),

    calorie_target: float = Form(...),
    protein_target: float = Form(...),

    chicken_percent: float = Form(0),
    pork_percent: float = Form(0),
    beef_percent: float = Form(0),
    egg_percent: float = Form(0),
    fish_percent: float = Form(0),
    whey_percent: float = Form(0),

    meal_style: str = Form("thai"),
):

    from core.food_engine import load_foods
    from core.god_engine import generate_week_plan
    from core.meal_suggester import suggest_meals

    foods_dict = load_foods()

    protein_split = {
        "chicken": chicken_percent,
        "pork": pork_percent,
        "beef": beef_percent,
        "egg": egg_percent,
        "fish": fish_percent,
        "whey": whey_percent,
    }

    foods = [
        {
            "name": name,
            "protein": data["protein"],
            "calories": data["calories"],
            "price": data["price"]
        }
        for name, data in foods_dict.items()
    ]

    week = generate_week_plan(
        foods,
        calorie_target,
        protein_target,
        protein_split,
        None
    )

    # ✅ Smart suggestion based on style
    for day in week:
        day["suggested_meals"] = suggest_meals(day, meal_style)

    return templates.TemplateResponse(
        "weekly_plan.html",
        {
            "request": request,
            "week": week,
            "meal_style": meal_style
        }
    )
