# -*- coding: utf-8 -*-

def build_trainer_summary(total_weeks, weekly_protein_planned, weekly_protein_target):
    
    if total_weeks == 0:
        title = "Getting Started"
        subtitle = "Start logging meals to unlock insights."
    
    elif weekly_protein_planned >= weekly_protein_target:
        title = "Protein Champion"
        subtitle = "You are consistently hitting your weekly protein goals."
    
    else:
        title = "Consistency Builder"
        subtitle = "You're building momentum. Stay consistent."

    return {
        "trainer_title": title,
        "trainer_subtitle": subtitle
    }
