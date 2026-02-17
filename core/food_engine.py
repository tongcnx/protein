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

    return results
