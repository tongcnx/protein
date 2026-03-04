def calculate_tdee(weight, height, age, gender, activity):

    # BMR (Mifflin-St Jeor)
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_map = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.725
    }

    tdee = bmr * activity_map.get(activity, 1.2)

    return tdee


def protein_target(weight, goal):

    goal_map = {
        "cut": 2.0,
        "maintain": 1.6,
        "bulk": 2.2
    }

    protein_day = weight * goal_map.get(goal, 1.6)

    protein_week = protein_day * 7

    return protein_day, protein_week