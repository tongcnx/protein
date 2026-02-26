class NutritionCalculator:

    @staticmethod
    def protein_target(weight, goal):

        if goal == "build":
            return weight * 2.0

        if goal == "cut":
            return weight * 1.8

        return weight * 1.5


    @staticmethod
    def calories(weight,height,age,activity):

        bmr = 10*weight + 6.25*height -5*age +5

        return bmr * activity