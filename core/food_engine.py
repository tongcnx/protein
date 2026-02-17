import json

def load_foods():
    with open("data/food_database.json", "r", encoding="utf-8") as f:
        return json.load(f)


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


    return results
