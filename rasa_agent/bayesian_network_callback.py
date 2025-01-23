  #!/usr/bin/env python
# coding: utf-8

import pyAgrum as gum
import itertools

def career_recommendation(interest, skill, background, lifestyle):


    bn = gum.BayesNet('CareerCoach')

    # User Preferences
    bn.add(gum.LabelizedVariable('Interest', 'Interest in field', 3)) 
    bn.add(gum.LabelizedVariable('Skill', 'Skill level', 3))  
    bn.add(gum.LabelizedVariable('Background', 'Educational Background', 3))  
    bn.add(gum.LabelizedVariable('Lifestyle', 'Preferred lifestyle', 3)) 

    # Career Choices
    bn.add(gum.LabelizedVariable('Career', 'Career options', 3)) 

    # Dependencies
    bn.addArc('Interest', 'Career')
    bn.addArc('Skill', 'Career')
    bn.addArc('Background', 'Career')
    bn.addArc('Lifestyle', 'Career')

    # Prior probabilities
    bn.cpt('Interest').fillWith([0.4, 0.3, 0.3])  
    bn.cpt('Skill').fillWith([0.3, 0.4, 0.3])    
    bn.cpt('Background').fillWith([0.5, 0.3, 0.2])  
    bn.cpt('Lifestyle').fillWith([0.4, 0.4, 0.2])  

    # Rules for probability assignments
    def assign_probabilities(interest, skill, background, lifestyle):
        if interest == 0 and skill == 0 and background == 0 and lifestyle == 0:
            return [0.9, 0.05, 0.05]  # Data Scientist
        elif interest == 1 and skill == 1 and background == 1 and lifestyle == 1:
            return [0.1, 0.8, 0.1]  # Writer
        elif interest == 1 and skill == 1 and background == 1 and lifestyle == 2:
            return [0.55, 0.8, 0.55]  # Writer
        elif interest == 2 and skill == 2 and background == 0 and lifestyle == 2:
            return [0.4, 0.2, 0.4]  # Balanced
        elif interest == 2 and skill == 2 and background == 0 and lifestyle == 0:
            return [0.4, 0.3, 0.3]  # Balanced
        elif interest == 2 and skill == 2 and background == 1 and lifestyle == 0:
            return [0.3, 0.3, 0.4]  # Manager
        elif interest == 0 and skill == 0 and background == 2 and lifestyle == 0:
            return [0.3, 0.3, 0.4]  # Manager
        elif interest == 0 and skill == 0 and background == 2 and lifestyle == 1:
            return [0.4, 0.3, 0.3]  # Data Scientist
        elif interest == 1 and skill == 1 and background == 0 and lifestyle == 0:
            return [0.55, 0.8, 0.55]  # Writer
        elif interest == 1 and skill == 1 and background == 0 and lifestyle == 1:
            return [0.4, 0.4, 0.2]  # Balanced
        elif interest == 2 and skill == 2 and background == 1 and lifestyle == 2:
            return [0.3, 0.3, 0.4]  # Manager
        elif interest == 0 and skill == 2 and background == 0 and lifestyle == 2:
            return [0.3, 0.3, 0.4]  # Manager
        elif interest == 0 and skill == 0 and background == 1 and lifestyle == 1:
            return [0.3, 0.3, 0.4]  # Manager
        elif interest == 1 and skill == 0 and background == 1 and lifestyle == 0:
            return [0.55, 0.4, 0.05]  # Writer
        elif interest == 1 and skill == 0 and background == 1 and lifestyle == 2:
            return [0.2, 0.75, 0.05]  # Writer
        elif interest == 0 and skill == 0 and background == 0 and lifestyle == 2:
            return [0.2, 0.3, 0.5]  # Manager
        elif interest == 0 and skill == 0 and background == 1 and lifestyle == 2:
            return [0.4, 0.3, 0.3]  # Balanced
        else:
            return [0.4, 0.3, 0.3]  # Default

    # CPTs for Career
    parent_combinations = itertools.product(
        range(3),  # Interest 
        range(3),  # Skill 
        range(3),  # Background 
        range(3)   # Lifestyle 
    )

    for interest, skill, background, lifestyle in parent_combinations:
        probabilities = assign_probabilities(interest, skill, background, lifestyle)
        bn.cpt('Career')[{'Interest': interest, 'Skill': skill, 'Background': background, 'Lifestyle': lifestyle}] = probabilities

    # Inference
    ie = gum.LazyPropagation(bn)

    # Evidence
    ie.setEvidence({'Interest': interest, 'Skill': skill, 'Background': background, 'Lifestyle': lifestyle})
    ie.makeInference()

    # Probabilities for career options
    career_options = ['Data Scientist', 'Writer', 'Manager']
    probabilities = ie.posterior('Career').tolist()

    # Rank
    ranked_careers = sorted(zip(career_options, probabilities), key=lambda x: x[1], reverse=True)
    print("\nCareer Rankings:")
    for rank, (career, prob) in enumerate(ranked_careers, start=1):
        print(f"Rank {rank}: {career} ({prob:.2f})")


    return [(career, round(prob, 2)) for career, prob in ranked_careers]
