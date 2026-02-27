from fastapi import APIRouter
from app.services.meal_generator import MealGenerator

router=APIRouter()

gen=MealGenerator()


@router.get("/generate_week")
def generate_week(protein:int):

    return gen.generate_week(protein)