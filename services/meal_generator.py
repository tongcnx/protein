from core.nutrition_engine import FoodEngine
import random

engine = FoodEngine()

class MealGenerator:


    def generate_day(self,target_protein):

        foods = engine.all_foods()

        plan=[]

        protein=0

        while protein < target_protein:

            f=random.choice(foods)

            plan.append({
                "food":f["name"],
                "gram":100
            })

            protein+=f["protein"]

        return plan


    def generate_week(self,target):

        week={}

        for d in range(7):

            week[d]=self.generate_day(target)

        return week