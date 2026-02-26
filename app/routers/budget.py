from fastapi import APIRouter
from services.budget_optimizer import BudgetOptimizer

router=APIRouter()

opt=BudgetOptimizer()


@router.get("/optimize")
def optimize(budget:int,protein:int):

    return opt.optimize(budget,protein)