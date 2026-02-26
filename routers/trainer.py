# -*- coding: utf-8 -*-

def build_trainer_summary(
    planned_protein,
    target_protein,
    total_cost,
    avg_cost
):
    """
    Generate AI trainer insight summary
    """

    # Safety check
    if target_protein == 0:
        consistency_ratio = 0
    else:
        consistency_ratio = planned_protein / target_protein

    # ===== Title Logic =====
    if planned_protein == 0:
        title = "Getting Started"
        subtitle = "Start logging meals to unlock insights."

    elif consistency_ratio >= 1:
        title = "Protein Champion"
        subtitle = "You are consistently hitting your protein goals."

    elif consistency_ratio >= 0.7:
        title = "Consistency Builder"
        subtitle = "You're building momentum. Stay consistent."

    else:
        title = "Needs Improvement"
        subtitle = "Focus on increasing daily protein intake."

    # ===== Cost Insight =====
    if avg_cost <= 60:
        cost_tip = "Great job keeping protein cost efficient."
    elif avg_cost <= 100:
        cost_tip = "Moderate cost efficiency. Room to optimize."
    else:
        cost_tip = "High protein cost. Consider budget-friendly options."

    return {
        "trainer_title": title,
        "trainer_subtitle": subtitle,
        "cost_insight": cost_tip
    }
