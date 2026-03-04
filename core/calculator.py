def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161


def calculate_tdee(bmr, activity_multiplier):
    return bmr * activity_multiplier


def protein_multiplier(goal):
    mapping = {
        "maintain": 1.4,
        "gain": 1.8,
        "cut": 2.2
    }
    return mapping.get(goal, 1.6)


def calculate_protein(weight, goal):
    multiplier = protein_multiplier(goal)
    daily = weight * multiplier
    weekly = daily * 7
    return daily, weekly
