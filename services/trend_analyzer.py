class TrendAnalyzer:


    def weight_trend(self,logs):

        return [x.weight for x in logs]


    def cost_trend(self,logs):

        return [x.cost for x in logs]