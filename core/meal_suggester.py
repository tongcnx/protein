import random

MEAL_DATABASE = {
    "thai": {
        "chicken": [
            "ผัดกะเพราไก่",
            "ไก่ผัดกระเทียม",
            "ข้าวมันไก่"
        ],
        "pork": [
            "หมูผัดกะเพรา",
            "หมูทอดกระเทียม",
        ],
        "egg": [
            "ไข่เจียว",
            "ไข่ต้ม + น้ำพริก"
        ],
    },

    "clean": {
        "chicken": [
            "Grilled Chicken Bowl",
            "Chicken Salad",
            "Chicken + Brown Rice"
        ],
        "pork": [
            "Lean Pork Bowl",
            "Grilled Pork + Veggies"
        ],
        "egg": [
            "Boiled Eggs + Salad",
            "Egg White Omelette"
        ],
    },

    "gym": {
        "chicken": [
            "High Protein Chicken Plate",
            "Chicken + Rice + Broccoli"
        ],
        "whey": [
            "Whey Protein Shake",
            "Banana Whey Smoothie"
        ],
        "egg": [
            "6 Egg Whites Omelette",
            "Egg + Oat Bowl"
        ],
    }
}


def suggest_meals(day_plan, style="thai"):

    if style not in MEAL_DATABASE:
        style = "thai"

    sorted_items = sorted(
        day_plan["menu"],
        key=lambda x: x["grams"],
        reverse=True
    )

    suggestions = []

    style_db = MEAL_DATABASE[style]

    for item in sorted_items[:2]:

        base = item["name"]

        if base in style_db:
            meals = style_db[base]
            suggestions.extend(random.sample(meals, min(2, len(meals))))

    suggestions = list(set(suggestions))

    return suggestions[:3]
