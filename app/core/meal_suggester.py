# core/meal_suggester.py

import random

PORTION_SIZE = 100  # 1 portion = 100g


MENU_DB = {
    "chicken": {
        "thai": [
            "ไก่ย่าง",
            "ต้มยำไก่",
            "ไก่ผัดพริก",
            "ข้าวมันไก่",
            "ลาบไก่",
        ]
    },
    "pork": {
        "thai": [
            "หมูย่าง",
            "หมูผัดกระเทียม",
            "ต้มแซ่บหมู",
            "ลาบหมู",
            "หมูทอด",
        ]
    },
    "beef": {
        "thai": [
            "เนื้อย่าง",
            "ผัดกะเพราเนื้อ",
            "ต้มเนื้อ",
            "เนื้อผัดพริกไทยดำ",
            "เนื้อตุ๋น",
        ]
    },
    "fish": {
        "thai": [
            "ปลานึ่งมะนาว",
            "ปลาทอด",
            "ต้มยำปลา",
            "ปลาย่าง",
            "ปลาผัดฉ่า",
        ]
    },
    "egg": {
        "thai": [
            "ไข่ต้ม",
            "ไข่เจียว",
            "ไข่ลูกเขย",
            "ไข่พะโล้",
            "ไข่ดาว",
        ]
    },
    "whey": {
        "thai": [
            "เวย์เชค",
            "เวย์ + กล้วย",
            "เวย์ + ข้าวโอ๊ต",
        ]
    },
}


def suggest_meals(day_plan, style="thai"):
    """
    Portion-based meal suggestion
    1 portion = 100g
    """

    suggestions = []

    for item in day_plan["menu"]:

        grams = item["grams"]
        name = item["name"]

        if grams <= 0:
            continue

        portions = int(grams // PORTION_SIZE)

        if portions <= 0:
            continue

        if name not in MENU_DB:
            continue

        if style not in MENU_DB[name]:
            continue

        meal_pool = MENU_DB[name][style]

        # เลือกตามจำนวน portion
        selected = random.sample(
            meal_pool,
            min(portions, len(meal_pool))
        )

        for meal in selected:
            suggestions.append({
                "food": name,
                "meal": meal,
                "portion_grams": PORTION_SIZE
            })

    return suggestions
