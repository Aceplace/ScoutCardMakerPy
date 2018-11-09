from defensiveformation.defensiveutils import *
from offensiveformation.formation import Formation

from defensiveformation.overplacementrule import *
from defensiveformation.alignmentplacementrule import *



class DefensiveEditorController:
    def __init__(self):
        self.current_defense = get_default_defense()
        self.current_formation = Formation()
        self.current_defender = self.current_defense.c

        self.placement_type_dict = {
                        'Alignment': (AlignmentPlacementRule, AlignmentPlacementRuleGUI),
                        'Over': (OverPlacementRule, OverPlacementRule)
                        }

    def get_defender_names(self):
        defenders = [label for label, defender in self.current_defense.defenders.items()]
        return defenders

    def get_placement_names(self):
        placement_rule_names = [label for label, rule_gui in self.placement_type_dict.items()]
        return placement_rule_names

    def get_placement_rule_name_from_placement_rule(self, placement_rule):
        for label, (placement_type_class, gui_class) in self.placement_type_dict.items():
            if type(placement_rule) == placement_type_class:
                return label
