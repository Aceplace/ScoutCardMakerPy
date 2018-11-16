from misc.scoutcardmakerexceptions import ScoutCardMakerException
from defensiveformation.defense import Defense
from defensiveformation.defensiveutils import *
import pickle

class DefensiveLibrary:
    def __init__(self):
        self.defenses = {}

    def add_defense_to_library(self, defense_name, defense):
        if len(defense_name.strip().split()) != 1:
            raise ScoutCardMakerException("Defensive name must be one word.")
        defense_name_upper = defense_name.strip().upper()

        #create defense to save and add it to the library
        defense_to_save = get_default_defense()
        defense_to_save.copy_defense_from_defense(defense)

        self.defenses[defense_name_upper] = defense_to_save

    def delete_defense_from_library(self, defense_to_delete):
        try:
            del self.defenses[defense_to_delete]
        except KeyError:
            raise ScoutCardMakerException(f'{defense_to_delete} not in defenses.')

    def save_library(self, filename):
        try:
            file_object = open(filename, 'wb')
            pickle.dump(self.defenses, file_object)
            file_object.close()
        except IOError as e:
            raise ScoutCardMakerException(str(e))

    def load_library(self, filename):
        try:
            file_object = open(filename, 'rb')
            defenses = pickle.load(file_object)
            self.defenses = defenses
        except IOError as e:
            raise ScoutCardMakerException(str(e))

    def get_defense(self, defense_name):
        defense = get_default_defense()
        defense.copy_defense_from_defense(self.defenses[defense_name])
        return defense

    def get_composite_defense(self, defense_name):
        defense_words = defense_name.strip().upper().split()

        #check that all defenses exist
        for defense_word in defense_words:
            if defense_word not in self.defenses:
                raise ScoutCardMakerException(defense_word + ' doesn\'t exist in library. Create it.')

        defense = get_default_defense()

        #copy all defense affects one at a time
        for defense_word in defense_words:
            defense.override_defense(self.defenses[defense_word])

        return defense

    def get_sorted_defense_names(self):
        return sorted([defense_name for defense_name in self.defenses.keys() ])
