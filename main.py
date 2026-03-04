from fastapi import FastAPI, Request, Form, Depends, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from collections import defaultdict
from datetime import datetime
import logging

from database import engine
from models import User, WeeklyRecord, MealPlan, MealItem, Base
from auth import hash_password, verify_password, create_access_token
from dependencies import get_current_user, get_db
from core.food_engine import generate_optimized_menu, load_foods
from core.god_engine import generate_week_plan
from core.meal_suggester import suggest_meals
from trainer import build_trainer_summary

# ================= Logging =================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nutrition-app")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ================= Helper =================

def generate_grocery_summary(mealplan):
    summary = defaultdict(lambda: {"amount": 0, "unit": ""})
    for item in mealplan.items:
        summary[item.food_name]["amount"] += item.amount
        summary[item.food_name]["unit"] = item.unit
    return summary

# ================= Auth =================

@app.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Passwords do not match"})

    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered"})

    db.add(User(email=email, password=hash_password(password)))
    db.commit()
    return RedirectResponse("/login", status_code=303)

@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid email or password"})

    token = create_access_token({"sub": user.email})
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie("token", token, httponly=True, samesite="none", secure=True)
    return response

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, token: str | None = Cookie(None)):
    if token:
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("token")
    return response

# ================= Dashboard =================

@app.get("/", response_class=HTMLResponse)
def root(token: str | None = Cookie(None)):
    if not token:
        return RedirectResponse("/login", status_code=303)
    return RedirectResponse("/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request})

# ================= Progress =================

@app.get("/progress", response_class=HTMLResponse)
def progress(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_obj = db.query(User).filter(User.email == user).first()
    records = db.query(WeeklyRecord).filter(
        WeeklyRecord.user_id == user_obj.id
    ).order_by(WeeklyRecord.created_at).all()

    labels = [r.created_at.strftime("%d %b") for r in records]
    estimated = [round(r.total_cost, 2) for r in records]
    actual = [round(r.actual_cost, 2) if r.actual_cost else None for r in records]

    return templates.TemplateResponse("progress.html", {
        "request": request,
        "records": records,
        "labels": labels,
        "estimated": estimated,
        "actual": actual
    })

# ================= Profile =================

@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_obj = db.query(User).filter(User.email == user).first()
    records = db.query(WeeklyRecord).filter(WeeklyRecord.user_id == user_obj.id).all()

    total_weeks = len(records)
    total_estimated = sum(r.total_cost for r in records)
    total_actual = sum(r.actual_cost for r in records if r.actual_cost)

    avg_estimated = total_estimated / total_weeks if total_weeks else 0
    avg_actual = total_actual / total_weeks if total_weeks else 0

    consistency_score = round((len([r for r in records if r.actual_cost]) / total_weeks) * 100) if total_weeks else 0

    trainer_summary = build_trainer_summary(
        total_estimated,
        total_estimated,
        total_estimated,
        avg_estimated
    )

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user_obj,
        "total_weeks": total_weeks,
        "avg_estimated": round(avg_estimated, 2),
        "avg_actual": round(avg_actual, 2),
        "consistency_score": consistency_score,
        "trainer_title": trainer_summary["trainer_title"],
        "trainer_subtitle": trainer_summary["trainer_subtitle"],
        "cost_insight": trainer_summary["cost_insight"]
    })

# ================= Menu Generator =================

@app.get("/menu-generator", response_class=HTMLResponse)
def menu_generator(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("menu.html", {"request": request})

@app.post("/generate-menu")
def generate_menu(
    request: Request,
    calorie_target: float = Form(...),
    protein_target: float = Form(...),
    budget: float = Form(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_obj = db.query(User).filter(User.email == user).first()

    result = generate_optimized_menu(calorie_target, protein_target, budget)

    mealplan = MealPlan(
        user_id=user_obj.id,
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
        db.add(MealItem(
            mealplan_id=mealplan.id,
            food_name=item["name"],
            amount=item.get("amount", 1),
            unit=item.get("unit", "unit"),
            calories=item["calories"],
            protein=item["protein"],
            cost=item["price"],
        ))

    db.commit()

    return templates.TemplateResponse("menu.html", {"request": request, "result": result})

# ================= God Mode =================

@app.post("/generate-god-mode")
def generate_god_mode(
    request: Request,
    calorie_target: float = Form(...),
    protein_target: float = Form(...),
):
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

    week = generate_week_plan(foods, calorie_target, protein_target, None, None)

    for day in week:
        day["suggested_meals"] = suggest_meals(day)

    return templates.TemplateResponse("menu.html", {"request": request, "week": week})

# ================= Grocery =================

@app.get("/grocery/{plan_id}")
def grocery_page(plan_id: int, request: Request, db: Session = Depends(get_db)):
    mealplan = db.query(MealPlan).filter(MealPlan.id == plan_id).first()
    summary = generate_grocery_summary(mealplan)
    return templates.TemplateResponse("grocery.html", {
        "request": request,
        "summary": summary,
        "mealplan": mealplan
    })

# ================= Health =================

@app.get("/health")
def health():
    return {"status": "ok"}
