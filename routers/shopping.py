from fastapi import APIRouter
from services.shopping_list import ShoppingList

router=APIRouter()

shop=ShoppingList()


@router.post("/shopping")
def shopping(plan:dict):

    return shop.generate(plan)