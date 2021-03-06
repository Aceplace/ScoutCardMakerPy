from defensiveformation.defensivelibrary import DefensiveLibrary
from defensiveformation.defensiveutils import *
from offensiveformation.formation import Formation

from offensiveformation.formationlibrary import FormationLibrary

from defensiveformation.placementrules.placementruleutils import *


class DefenseController:
    def __init__(self):
        self.current_defense = get_default_defense()
        self.current_formation = Formation()
        self.formation_library = FormationLibrary()
        self.current_defender = self.current_defense.c
        self.defense_library = DefensiveLibrary()
        self.editor = None


    def get_defender_names(self):
        defenders = [label for label, defender in self.current_defense.defenders.items()]
        return defenders

    def get_placement_names(self):
        placement_rule_names = [label for label, rule_gui in placement_type_dict.items()]
        return placement_rule_names

    def get_placement_names_without_conditional(self):
        placement_rule_names = [label for label, rule_gui in placement_type_dict.items() if label !='Conditional']
        return placement_rule_names

    def get_placement_rule_name_from_placement_rule(self, placement_rule):
        for label, placement_type_class in placement_type_dict.items():
            if type(placement_rule) == placement_type_class:
                return label

    def set_current_defender(self, label):
        self.current_defender = self.current_defense.defenders[label]

    def change_placement_rule(self, placement_rule_name):
        self.current_defender.placement_rule = placement_type_dict[placement_rule_name]()

    def checked_affected_defenders_box(self, affected_defender_tags):
        self.current_defense.affected_defender_tags = affected_defender_tags
        if hasattr(self, 'view'):
            self.view.update_view()

    def set_defender_placement_rule(self, placement_rule):
        self.current_defender.placement_rule = placement_rule
        if hasattr(self, 'view'):
            self.view.update_view()

    def update_view(self):
        if hasattr(self, 'view'):
            self.view.update_view()

    def get_placement_rule_gui(self, root):
        return placement_type_gui_dict[type(self.current_defender.placement_rule)](root, self)

    def get_placement_rule_gui_class_from_placement_rule(self, placement_rule):
        return placement_type_gui_dict[type(placement_rule)]

    def get_current_defender_placement_rule_name(self):
        return placement_type_name_dict[type(self.current_defender.placement_rule)]

    def get_placement_rule_from_name(self, placement_rule_name):
        return placement_type_dict[placement_rule_name]()

    def get_placement_type_name_from_placement_rule(self, placement_rule):
        return placement_type_name_dict[type(placement_rule)]

    def load_offensive_formation(self, formation_name):
        self.current_formation = self.formation_library.get_composite_formation(formation_name)

    def save_defense_to_library(self, defense_name, affected_defender_tags):
        self.current_defense.affected_defender_tags = affected_defender_tags
        self.defense_library.add_defense_to_library(defense_name, self.current_defense)

    def load_composite_defense_from_library(self, defense_name):
        defense = self.defense_library.get_composite_defense(defense_name)
        self.current_defense.copy_defense_from_defense(defense)

    def delete_defense_from_library(self, defense_name):
        self.defense_library.delete_defense_from_library(defense_name)

    def load_defense_from_library(self, defense_name):
        defense = self.defense_library.get_defense(defense_name)
        self.current_defense.copy_defense_from_defense(defense)

    def load_formation_library(self, file_name):
        self.formation_library.load_library(file_name)

    def set_formation_library(self, formation_library):
        self.formation_library = formation_library

    def load_defense_library(self, file_name):
        self.defense_library.load_library(file_name)
        if self.editor:
            self.editor.refresh_library()

    def new_defense_library(self):
        self.defense_library = DefensiveLibrary()
        if self.editor:
            self.editor.refresh_library()

    def save_defense_library(self, library_filename):
        self.defense_library.save_library(library_filename)




