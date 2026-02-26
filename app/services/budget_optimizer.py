from core.nutrition_engine import FoodEngine

engine=FoodEngine()

class BudgetOptimizer:


    def optimize(self,budget,protein_target):

        foods=engine.all_foods()

        foods.sort(key=lambda x: x["price"]/x["protein"])

        result=[]

        protein=0
        cost=0

        for f in foods:

            if protein>=protein_target:

                break

            gram=200

            p=f["protein"]*gram/100

            c=f["price"]*gram/1000

            if cost+c>budget:

                continue

            result.append({
                "food":f["name"],
                "gram":gram
            })

            protein+=p
            cost+=c

        return {

            "plan":result,
            "protein":protein,
            "cost":cost

        }