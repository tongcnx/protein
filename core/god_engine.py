import random

def generate_day_plan(food_data, calorie_target, protein_target, budget=None):

    expanded_foods = []

    # สร้างหลาย portion
    for food in food_data:
        for portion in [0.5, 1, 1.5, 2]:
            expanded_foods.append({
                "name": f"{food['name']} x{portion}",
                "calories": food["calories"] * portion,
                "protein": food["protein"] * portion,
                "price": food["price"] * portion,
                "base": food["name"]
            })

    # คำนวณ score
    for f in expanded_foods:
        protein_score = (f["protein"] / f["price"]) * f.get("weight_factor", 1)
        calorie_penalty = abs(calorie_target - f["calories"])
        f["score"] = protein_score - (calorie_penalty * 0.001)

    expanded_foods.sort(key=lambda x: x["score"], reverse=True)

    total_cal = 0
    total_protein = 0
    total_cost = 0
    menu = []
    used = set()

    for food in expanded_foods:

        if total_protein >= protein_target:
            break

        if food["base"] in used:
            continue

        if total_cal + food["calories"] > calorie_target:
            continue

        if budget and (total_cost + food["price"] > budget):
            continue

        menu.append(food)
        used.add(food["base"])
        total_cal += food["calories"]
        total_protein += food["protein"]
        total_cost += food["price"]

    return {
        "menu": menu,
        "total_cal": round(total_cal, 2),
        "total_protein": round(total_protein, 2),
        "total_cost": round(total_cost, 2),
    }


def generate_week_plan(food_data, calorie_target, protein_target, budget=None):
    week = []
    history = set()

    for _ in range(7):
        day = generate_day_plan(food_data, calorie_target, protein_target, budget)

        # กันซ้ำข้ามวัน
        for item in day["menu"]:
            history.add(item["base"])

        week.append(day)

    return week
