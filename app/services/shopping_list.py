def generate_shopping(portfolio):

    shopping=[]

    for item in portfolio:

        shopping.append({
            "source_id":item["source_id"],
            "grams":item["grams"]
        })

    return shopping