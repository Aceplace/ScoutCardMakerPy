from defensiveformation.defensiveutils import *
from offensiveformation.formation import Formation

from defensiveformation.overplacementrule import *
from defensiveformation.alignmentplacementrule import *

from misc.scoutcardmakerexceptions import ScoutCardMakerException
from offensiveformation.formationlibrary import FormationLibrary


class DefensiveEditorController:
    def __init__(self):
        self.current_defense = get_default_defense()
        self.current_formation = Formation()
        self.current_formation_library = FormationLibrary()
        self.current_defender = self.current_defense.c

        self.placement_type_dict = {
                        'Alignment': (AlignmentPlacementRule, AlignmentPlacementRuleGUI),
                        'Over': (OverPlacementRule, OverPlacementRuleGUI)
                        }

        self.placement_type_gui_dict = {
                        AlignmentPlacementRule: AlignmentPlacementRuleGUI,
                        OverPlacementRule: OverPlacementRuleGUI
                        }

        self.placement_type_name_dict = {
                        AlignmentPlacementRule: 'Alignment',
                        OverPlacementRule: 'Over'
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

    def set_current_defender(self, label):
        self.current_defender = self.current_defense.defenders[label]

    def change_placement_rule(self, placement_rule_name):
        self.current_defender.placement_rule = self.placement_type_dict[placement_rule_name][0]()

    def set_defender_placement_rule(self, placement_rule):
        self.current_defender.placement_rule = placement_rule
        if hasattr(self, 'view'):
            self.view.update_view()

    def get_placement_rule_gui(self, root):
        return self.placement_type_gui_dict[type(self.current_defender.placement_rule)](root, self)

    def get_current_defender_placement_rule_name(self):
        return self.placement_type_name_dict[type(self.current_defender.placement_rule)]


    def load_offensive_formation(self, formation_name):
        self.current_formation = self.current_formation_library.get_composite_formation(formation_name)


