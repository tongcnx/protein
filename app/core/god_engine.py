# core/god_engine.py

ROUND_UNIT = 100


def round_100g(x):
    return int(round(x / ROUND_UNIT)) * ROUND_UNIT


def generate_day_plan(
    food_data,
    calorie_target,
    protein_target,
    protein_split,
    budget=None,
):
    food_lookup = {f["name"]: f for f in food_data}

    plan = []
    total_cal = 0
    total_protein = 0
    total_cost = 0

    for food in food_data:

        name = food["name"]
        percent = protein_split.get(name, 0) / 100

        if percent <= 0:
            continue

        # 🎯 target protein per source
        protein_needed = protein_target * percent

        # 🎯 convert to grams
        raw_grams = (protein_needed / food["protein"]) * 100

        grams = round_100g(raw_grams)

        calories = (grams / 100) * food["calories"]
        protein = (grams / 100) * food["protein"]
        cost = (grams / 100) * food["price"]

        total_cal += calories
        total_protein += protein
        total_cost += cost

        plan.append({
            "name": name,
            "grams": grams,
            "calories": round(calories, 2),
            "protein": round(protein, 2),
            "cost": round(cost, 2),
        })

    # 🔒 Calorie constraint
    if total_cal > calorie_target:
        reduction_ratio = calorie_target / total_cal

        total_cal = 0
        total_protein = 0
        total_cost = 0

        for item in plan:
            new_grams = round_100g(item["grams"] * reduction_ratio)
            item["grams"] = new_grams

            food = food_lookup[item["name"]]

            item["calories"] = round((new_grams / 100) * food["calories"], 2)
            item["protein"] = round((new_grams / 100) * food["protein"], 2)
            item["cost"] = round((new_grams / 100) * food["price"], 2)

            total_cal += item["calories"]
            total_protein += item["protein"]
            total_cost += item["cost"]

    # 🔒 Budget constraint
    if budget and total_cost > budget:
        reduction_ratio = budget / total_cost

        total_cal = 0
        total_protein = 0
        total_cost = 0

        for item in plan:
            new_grams = round_100g(item["grams"] * reduction_ratio)
            item["grams"] = new_grams

            food = food_lookup[item["name"]]

            item["calories"] = round((new_grams / 100) * food["calories"], 2)
            item["protein"] = round((new_grams / 100) * food["protein"], 2)
            item["cost"] = round((new_grams / 100) * food["price"], 2)

            total_cal += item["calories"]
            total_protein += item["protein"]
            total_cost += item["cost"]

    return {
        "menu": sorted(plan, key=lambda x: x["grams"], reverse=True),
        "total_cal": round(total_cal, 2),
        "total_protein": round(total_protein, 2),
        "total_cost": round(total_cost, 2),
    }


def generate_week_plan(
    food_data,
    calorie_target,
    protein_target,
    protein_split,
    budget=None,
):
    week = []

    for _ in range(7):
        day = generate_day_plan(
            food_data,
            calorie_target,
            protein_target,
            protein_split,
            budget,
        )
        week.append(day)

    return week
