def generate_day_plan(food_data, calorie_target, protein_target, protein_split, budget=None):

    plan = []
    total_cal = 0
    total_protein = 0
    total_cost = 0

    for food in food_data:

        name = food["name"]
        percent = protein_split.get(name, 0) / 100

        if percent <= 0:
            continue

        # 🎯 protein target per source
        protein_needed = protein_target * percent

        # 🎯 grams required
        grams = (protein_needed / food["protein"]) * 100

        calories = (grams / 100) * food["calories"]
        cost = (grams / 100) * food["price"]

        total_cal += calories
        total_protein += protein_needed
        total_cost += cost

        plan.append({
            "name": name,
            "grams": round(grams, 1),
            "calories": round(calories, 1),
            "protein": round(protein_needed, 1),
            "cost": round(cost, 1)
        })

    # 🔒 Constraint check
    if total_cal > calorie_target:
        reduction_ratio = calorie_target / total_cal

        for item in plan:
            item["grams"] *= reduction_ratio
            item["calories"] *= reduction_ratio
            item["protein"] *= reduction_ratio
            item["cost"] *= reduction_ratio

        total_cal *= reduction_ratio
        total_protein *= reduction_ratio
        total_cost *= reduction_ratio

    if budget and total_cost > budget:
        reduction_ratio = budget / total_cost

        for item in plan:
            item["grams"] *= reduction_ratio
            item["calories"] *= reduction_ratio
            item["protein"] *= reduction_ratio
            item["cost"] *= reduction_ratio

        total_cal *= reduction_ratio
        total_protein *= reduction_ratio
        total_cost *= reduction_ratio

    return {
        "menu": plan,
        "total_cal": round(total_cal, 2),
        "total_protein": round(total_protein, 2),
        "total_cost": round(total_cost, 2),
    }


def generate_week_plan(food_data, calorie_target, protein_target, protein_split, budget=None):

    week = []

    for _ in range(7):
        day = generate_day_plan(
            food_data,
            calorie_target,
            protein_target,
            protein_split,
            budget
        )
        week.append(day)

    return week
