def generate_menu(portfolio):

    menus=[]

    for item in portfolio:

        menus.append({
            "name":"Protein Meal",
            "protein":item["protein"]/7
        })

    return menus