import json

def load_foods():
    return {
        "chicken": {
            "protein": 31,
            "calories": 165,
            "price": 60
        },
        "pork": {
            "protein": 27,
            "calories": 242,
            "price": 80
        },
        "beef": {
            "protein": 26,
            "calories": 250,
            "price": 120
        },
        "egg": {
            "protein": 6,
            "calories": 70,
            "price": 5
        },
        "fish": {
            "protein": 22,
            "calories": 206,
            "price": 90
        },
        "whey": {
            "protein": 24,
            "calories": 120,
            "price": 35
        }
    }



def calculate_food_requirements(weekly_protein):
    foods = load_foods()
    results = []

    for food in foods:
        protein_per_unit = food["protein"]
        unit = food["unit"]

        amount_needed = weekly_protein / protein_per_unit

        results.append({
            "name": food["name"],
            "amount": round(amount_needed, 2),
            "unit": unit
        })

def calculate_portfolio(weekly_protein, food_percentages, meals_per_day):
    foods = load_foods()
    results = []

    for food in foods:
        name = food["name"]
        protein_per_unit = food["protein"]
        unit = food["unit"]

        percent = food_percentages.get(name, 0) / 100

        if percent > 0:
            protein_from_source = weekly_protein * percent
            weekly_amount = protein_from_source / protein_per_unit
            daily_amount = weekly_amount / 7
            per_meal_amount = daily_amount / meals_per_day

            results.append({
                "name": name,
                "weekly_amount": round(weekly_amount, 2),
                "daily_amount": round(daily_amount, 2),
                "per_meal_amount": round(per_meal_amount, 2),
                "unit": unit
            })

    return results

def generate_optimized_menu(calorie_target, protein_target, budget=None):
    foods = load_foods()

    foods = sorted(
        foods,
        key=lambda x: x["protein"] / x["price"],
        reverse=True
    )

    total_cal = 0
    total_protein = 0
    total_cost = 0
    menu = []

    for food in foods:
        while (
            total_protein < protein_target
            and total_cal + food.get("calories", 0) <= calorie_target
        ):
            if budget and (total_cost + food["price"] > budget):
                break

            menu.append(food)
            total_cal += food.get("calories", 0)
            total_protein += food["protein"]
            total_cost += food["price"]

    return {
        "menu": menu,
        "total_cal": round(total_cal, 2),
        "total_protein": round(total_protein, 2),
        "total_cost": round(total_cost, 2),
    }
