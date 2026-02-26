class ShoppingList:


    def generate(self,week_plan):

        result={}

        for day in week_plan.values():

            for item in day:

                name=item["food"]

                gram=item["gram"]

                if name not in result:

                    result[name]=0

                result[name]+=gram

        return result