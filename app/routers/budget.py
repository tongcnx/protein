from fastapi import APIRouter
from app.services.budget_optimizer import BudgetOptimizer

router=APIRouter()

opt=BudgetOptimizer()


@router.get("/optimize")
def optimize(budget:int,protein:int):

    return opt.optimize(budget,protein)