class TrainerEngine:


    def analyze(self,profile):

        tips=[]

        if profile["protein"]<profile["target"]:

            tips.append("Increase protein intake")

        if profile["weight_change"]>1:

            tips.append("Weight increasing too fast")

        return tips