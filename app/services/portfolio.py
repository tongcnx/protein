import random

def generate_portfolio(db, user_id, plan_id, protein_target):

    sources = db.execute("""
    SELECT ps.id, ps.protein_per_100g
    FROM protein_sources ps
    WHERE ps.enabled = TRUE
    AND ps.id NOT IN (
        SELECT source_id
        FROM user_restrictions
        WHERE user_id=:uid
    )
    """,{"uid":user_id}).fetchall()

    n = len(sources)

    per_source = protein_target / n

    portfolio=[]

    for s in sources:

        protein=per_source

        grams = protein / s.protein_per_100g *100

        portfolio.append({
            "source_id":s.id,
            "protein":protein,
            "grams":grams
        })

    return portfolio