from offensiveformation.formation import Formation
from misc.scoutcardmakerexceptions import ScoutCardMakerException
import pickle

class FormationLibrary:
    def __init__(self):
        self.formations = {}

    def add_formation_to_library(self, formation_name, formation):
        formation_words = formation_name.strip().upper().split()

        #automatically make direction right if they they don't specify it
        if len(formation_words) == 1:
            formation_words.append('RT')

        #Check that formation name has only two words
        if len(formation_words) != 2:
            raise ScoutCardMakerException("Formation names must be made up one word and a direction.")
        #check that the last word is either lt or rt
        if formation_words[1] != 'LT' and formation_words[1] != 'RT':
            raise ScoutCardMakerException('Name must end in LT or RT')

        #check that no other words are LT or RT
        if formation_words[0] == 'LT' or formation_words[0] == 'RT':
                raise ScoutCardMakerException('Name can\'t contain LT or RT except to specify direction')

        #construct formation name from the words
        modified_formation_name = ' '.join(formation_words)

        #construct a flipped formation name as well
        if formation_words[-1] == 'LT':
            formation_words[-1] =  'RT'
        else:
            formation_words[-1] = 'LT'

        flipped_modified_formation_name = ' '.join(formation_words)

        #create two formations and add them to the library
        formation_to_save = Formation()
        formation_to_save.copy_formation_from_formation(formation)
        flipped_formation_to_save = Formation()
        flipped_formation_to_save.copy_formation_from_formation(formation)
        flipped_formation_to_save.flip_formation()

        self.formations[modified_formation_name] = formation_to_save
        self.formations[flipped_modified_formation_name] = flipped_formation_to_save

    def does_formation_exist(self, formation_name):
        return formation_name in self.formations

    def delete_formation_from_library(self, formation_name):
        formation_words = formation_name.strip().upper().split()
        formation_to_delete = formation_name
        opposite_formation_to_delete = None
        if formation_words[-1] == 'LT':
            opposite_formation_to_delete = ' '.join([formation_words[0], 'RT'])
        elif formation_words[-1] == 'RT':
            opposite_formation_to_delete = ' '.join([formation_words[0], 'LT'])
        else:
            raise ScoutCardMakerException('Can\'t delete formation that doesn\'t end in LT or RT')

        try:
            del self.formations[formation_to_delete]
        except KeyError:
            raise ScoutCardMakerException(f'{formation_to_delete} not in formations.')

        try:
            del self.formations[opposite_formation_to_delete]
        except KeyError:
            raise ScoutCardMakerException(f'{opposite_formation_to_delete} not in formations.')


    def save_library(self, filename):
        try:
            with open(filename, 'wb') as file_object:
                pickle.dump(self.formations, file_object)
        except IOError as e:
            raise ScoutCardMakerException(str(e))

    def load_library(self, filename):
        try:
            with open(filename, 'rb') as file_object:
                formations = pickle.load(file_object)
                self.formations = formations
        except IOError as e:
            raise ScoutCardMakerException(str(e))

    def get_formation(self, formation_name):
        if not self.formations:
            raise ScoutCardMakerException('Formation Library Empty')

        formation = Formation()
        formation.copy_formation_from_formation(self.formations[formation_name])
        return formation


    def get_composite_formation(self, formation_name):
        if not self.formations:
            raise ScoutCardMakerException('Formation Library Empty')

        formation_words = formation_name.strip().upper().split()

        #determine if going lt or rt
        direction = None
        if 'LT' in formation_words and 'RT' not in formation_words:
            direction = 'LT'
        elif 'LT' not in formation_words and 'RT' in formation_words:
            direction = 'RT'
        else:
            raise ScoutCardMakerException('Can\'t determine if going Lt or Rt from formation name: ' + formation_name)

        sub_formation_names = [word + ' ' + direction for word in formation_words if word != 'LT' and word != 'RT']

        #check that all sub_formations exist
        for sub_formation_name in sub_formation_names:
            if sub_formation_name not in self.formations:
                raise ScoutCardMakerException(sub_formation_name + ' doesn\'t exist in library. Create it.')

        formation = Formation()

        #copy all formations affects one at a time
        for sub_formation_name in sub_formation_names:
            formation.override_formation(self.formations[sub_formation_name])

        return formation

    def get_sorted_formation_names(self):
        return sorted([formation_name for formation_name in self.formations.keys() ])

    def get_sorted_formation_names_right(self):
        return sorted([formation_name for formation_name in self.formations.keys() if formation_name.split()[-1] == 'RT'])

    def get_sorted_formation_names_no_direction(self):
        return sorted([formation_name.split()[0] for formation_name in self.formations.keys() if formation_name.split()[-1] == 'RT'])

