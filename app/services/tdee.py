def calculate_tdee(weight, height, age, gender, activity):

    if gender == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    return bmr * activity

def weekly_protein(tdee):

    protein_day = tdee * 0.30 / 4

    return protein_day * 7