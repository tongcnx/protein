# core/food_engine.py

def load_foods():
    return {
        "chicken": {"protein": 31, "calories": 165, "price": 60},
        "pork": {"protein": 27, "calories": 242, "price": 80},
        "beef": {"protein": 26, "calories": 250, "price": 120},
        "egg": {"protein": 6, "calories": 70, "price": 5},
        "fish": {"protein": 22, "calories": 206, "price": 90},
        "whey": {"protein": 24, "calories": 120, "price": 35},
    }


def generate_optimized_menu(calorie_target, protein_target, budget=None):
    foods_dict = load_foods()

    food_list = [
        {"name": name, **data}
        for name, data in foods_dict.items()
    ]

    # เรียงตาม protein per cost
    food_list = sorted(
        food_list,
        key=lambda x: x["protein"] / x["price"],
        reverse=True
    )

    total_cal = 0
    total_protein = 0
    total_cost = 0
    menu = []

    for food in food_list:
        while (
            total_protein < protein_target
            and total_cal + food["calories"] <= calorie_target
        ):
            if budget and total_cost + food["price"] > budget:
                break

            menu.append(food)
            total_cal += food["calories"]
            total_protein += food["protein"]
            total_cost += food["price"]

    return {
        "menu": menu,
        "total_cal": round(total_cal, 2),
        "total_protein": round(total_protein, 2),
        "total_cost": round(total_cost, 2),
    }
