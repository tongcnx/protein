import random

MEAL_DATABASE = {
    "chicken": [
        "Grilled Chicken Bowl",
        "Chicken Basil Stir Fry",
        "Chicken Garlic Rice",
        "Chicken Omelette"
    ],
    "pork": [
        "Pork Basil",
        "Grilled Pork Plate",
        "Pork Fried Rice"
    ],
    "egg": [
        "Omelette Rice",
        "Boiled Eggs with Salad",
        "Scrambled Eggs Bowl"
    ],
    "fish": [
        "Grilled Fish Plate",
        "Fish Salad",
        "Fish Rice Bowl"
    ],
    "beef": [
        "Beef Stir Fry",
        "Grilled Beef Bowl"
    ],
    "whey": [
        "Protein Shake",
        "Banana Whey Smoothie"
    ]
}


def suggest_meals(day_plan):

    # เรียง ingredient ตาม grams มากสุด
    sorted_items = sorted(
        day_plan["menu"],
        key=lambda x: x["grams"],
        reverse=True
    )

    suggestions = []

    # ใช้ top 2 ingredient เป็นหลัก
    for item in sorted_items[:2]:

        base = item["name"]

        if base in MEAL_DATABASE:
            meals = MEAL_DATABASE[base]
            suggestions.extend(random.sample(meals, min(2, len(meals))))

    # ลบซ้ำ
    suggestions = list(set(suggestions))

    return suggestions[:3]
