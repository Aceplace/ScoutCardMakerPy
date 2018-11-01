from formation import Formation
from scoutcardmakerexceptions import ScoutCardMakerException
import pickle

class FormationLibrary:
    def __init__(self):
        self.formations = {}

    def add_formation_to_library(self, formation_name, formation):
        formation_words = formation_name.strip().upper().split()
        #check that all words are alpha numeric
        # for word in formation_words:
        #     if not word.isalnum():
        #         raise ScoutCardMakerException('Name must contain only letters or numbers')

        #Check that formation name has only two words
        if len(formation_words) != 2:
            raise ScoutCardMakerException("Formation names must be made up of two words.")
        #check that the last word is either lt or rt
        if formation_words[1] != 'LT' and formation_words[1] != 'RT':
            raise ScoutCardMakerException('Name must end in LT or RT')

        #check that no other words are LT or RT
        if formation_words[0] == 'LT' or formation_words[0] == 'RT':
                raise ScoutCardMakerException('Name can\'t contain LT or RT except at the end')

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
        file_object = open(filename, 'wb')
        pickle.dump(self.formations, file_object)
        file_object.close()

    def load_library(self, filename):
        file_object = open(filename, 'rb')
        self.formations = pickle.load(file_object)

    def get_formation(self, formation_name):
        formation = Formation()
        formation.copy_formation_from_formation(self.formations[formation_name])
        return formation


    def get_composite_formation(self, formation_name):
        formation_words = formation_words = formation_name.strip().upper().split()

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

        #find the base formation and create a formation from that
        base_formation = None
        for sub_formation_name in sub_formation_names:
            if not self.formations[sub_formation_name].is_override_formation:
                if base_formation != None:
                    raise ScoutCardMakerException('Only one formation can be a non-override formation.')
                base_formation = self.formations[sub_formation_name]
        if base_formation == None:
            raise ScoutCardMakerException('Must contain one non-override formation.')

        formation = Formation()
        formation.copy_formation_from_formation(base_formation)

        #perform all override formations
        for sub_formation_name in sub_formation_names:
            if self.formations[sub_formation_name].is_override_formation:
                formation.override_formation(self.formations[sub_formation_name])

        return formation

    def get_sorted_formation_names(self):
        return sorted([formation_name for formation_name in self.formations.keys() ])

    def get_sorted_formation_names_right(self):
        return sorted([formation_name for formation_name in self.formations.keys() if formation_name.split()[-1] == 'RT'])

if __name__ == '__main__':
    library = FormationLibrary()

    formation = Formation()
    library.add_formation_to_library('Pro Rt', formation)

    formation.z.x = -28
    library.add_formation_to_library('Twin Lt', formation)

    formation.h.x = 8
    formation.is_override_formation = True
    formation.override_player_tags = ['T','H']
    library.add_formation_to_library('King Rt', formation)

    formation.q.y = 5
    formation.is_override_formation = True
    formation.override_player_tags = ['Q']
    library.add_formation_to_library('Gun Rt', formation)
    #library.load_library('formations.scmfl')

    for label, formation in library.formations.items():
        print('\n')
        print(label)
        print('Overide Formation : {}'.format(formation.is_override_formation))
        for label, player in formation.players.items():
            print('{}: {},{}'.format(player.label, player.x, player.y))

    library.save_library('formations.scmfl')
