import json

class FoodEngine:

    def __init__(self):

        with open("app/data/food_database.json") as f:
            self.foods = json.load(f)


    def all_foods(self):

        return self.foods


    def protein_of(self,name,gram):

        for f in self.foods:

            if f["name"] == name:

                return f["protein"] * gram / 100

        return 0


    def cost_of(self,name,gram):

        for f in self.foods:

            if f["name"] == name:

                return f["price"] * gram / 1000

        return 0