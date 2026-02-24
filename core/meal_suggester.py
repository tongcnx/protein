# core/meal_suggester.py

import random

MENU_DB = {
    "chicken": {
        "thai": [
            "ไก่ย่าง 200g",
            "ต้มยำไก่ 200g",
            "ไก่ผัดพริก 200g",
            "ข้าวมันไก่ 200g",
            "ลาบไก่ 200g",
        ]
    },
    "pork": {
        "thai": [
            "หมูย่าง 200g",
            "หมูผัดกระเทียม 200g",
            "ต้มแซ่บหมู 200g",
            "ลาบหมู 200g",
            "หมูทอด 200g",
        ]
    },
    "beef": {
        "thai": [
            "เนื้อย่าง 200g",
            "ผัดกะเพราเนื้อ 200g",
            "ต้มเนื้อ 200g",
            "เนื้อผัดพริกไทยดำ 200g",
            "เนื้อตุ๋น 200g",
        ]
    },
    "fish": {
        "thai": [
            "ปลานึ่งมะนาว 200g",
            "ปลาทอด 200g",
            "ต้มยำปลา 200g",
            "ปลาย่าง 200g",
            "ปลาผัดฉ่า 200g",
        ]
    },
    "egg": {
        "thai": [
            "ไข่ต้ม 2 ฟอง",
            "ไข่เจียว 2 ฟอง",
            "ไข่ลูกเขย",
            "ไข่พะโล้",
            "ไข่ดาว 2 ฟอง",
        ]
    },
    "whey": {
        "thai": [
            "เวย์เชค 1 scoop",
            "เวย์ + กล้วย",
            "เวย์ + ข้าวโอ๊ต",
        ]
    },
}


def suggest_meals(day_plan, style="thai"):

    sorted_items = sorted(
        day_plan["menu"],
        key=lambda x: x["grams"],
        reverse=True,
    )

    suggestions = []

    # ใช้ top 2 protein
    for item in sorted_items[:2]:

        base = item["name"]

        if base in MENU_DB and style in MENU_DB[base]:
            meals = MENU_DB[base][style]
            suggestions.extend(
                random.sample(meals, min(2, len(meals)))
            )

    # ลบซ้ำ
    suggestions = list(set(suggestions))

    return suggestions[:4]
