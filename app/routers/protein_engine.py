from fastapi import APIRouter,Depends
from app.database.database import SessionLocal
from app.services.tdee import calculate_tdee
from app.services.portfolio import generate_portfolio
from app.services.menu_generator import generate_menu
from app.services.shopping_list import generate_shopping

router=APIRouter()


@router.post("/generate-plan")

def generate_plan(user_id:int):

    db=SessionLocal()

    user=db.execute("""
    SELECT * FROM users
    WHERE id=:uid
    """,{"uid":user_id}).fetchone()

    tdee=calculate_tdee(
        user.weight,
        user.height,
        user.age,
        user.gender,
        user.activity_level
    )

    protein_week=tdee*0.3/4*7


    plan=db.execute("""
    INSERT INTO weekly_plans
    (user_id,tdee,protein_target)
    VALUES(:u,:t,:p)
    RETURNING id
    """,{
        "u":user_id,
        "t":tdee,
        "p":protein_week
    }).fetchone()

    plan_id=plan.id


    portfolio=generate_portfolio(
        db,
        user_id,
        plan_id,
        protein_week
    )


    for p in portfolio:

        db.execute("""
        INSERT INTO portfolio
        (plan_id,source_id,protein_amount,grams_amount)
        VALUES(:p,:s,:pa,:ga)
        """,{
            "p":plan_id,
            "s":p["source_id"],
            "pa":p["protein"],
            "ga":p["grams"]
        })


    db.commit()


    menu=generate_menu(portfolio)

    shopping=generate_shopping(portfolio)


    return {
        "tdee":tdee,
        "protein_week":protein_week,
        "portfolio":portfolio,
        "menu":menu,
        "shopping":shopping
    }