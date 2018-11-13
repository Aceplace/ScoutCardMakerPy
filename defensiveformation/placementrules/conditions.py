from offensiveformation.formationutils import get_formation_structure

condition_name_condition_evaluate_dict ={
    'Default': lambda formation: True,
    'Formation Structure: 1x1' : lambda formation: formation_structure_condition(formation, '1x1'),
    'Formation Structure: 2x1' : lambda formation: formation_structure_condition(formation, '2x1'),
    'Formation Structure: 2x2' : lambda formation: formation_structure_condition(formation, '2x2'),
    'Formation Structure: 3x1' : lambda formation: formation_structure_condition(formation, '3x1'),
    'Formation Structure: 3x2' : lambda formation: formation_structure_condition(formation, '3x2'),
    'Formation Structure: 4x1' : lambda formation: formation_structure_condition(formation, '4x1')
}

def formation_structure_condition(formation, formation_structure):
    return formation_structure == get_formation_structure(formation)