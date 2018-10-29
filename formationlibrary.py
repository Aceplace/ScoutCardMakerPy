from formation import Formation
from scoutcardmakerexceptions import ScoutCardMakerException
import pickle

class FormationLibrary:
    def __init__(self):
        self.formations = {}

    def add_formation_to_library(self, formation_name, formation):
        formation_words = formation_name.strip().upper().split()
        #check that all words are alpha numeric
        for word in formation_words:
            if not word.isalnum():
                raise ScoutCardMakerException('Name must contain only letters or numbers')

        #check that the last word is either lt or rt
        if formation_words[-1] != 'LT' and formation_words[-1] != 'RT':
            raise ScoutCardMakerException('Name must end in LT or RT')

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

    def save_library(self, filename):
        file_object = open(filename, 'wb')
        pickle.dump(self.formations, file_object)
        file_object.close()

    def load_library(self, filename):
        file_object = open(filename, 'rb')
        self.formations = pickle.load(file_object)

if __name__ == '__main__':
    library = FormationLibrary()

    # formation = Formation()
    # library.add_formation_to_library('Pro Rt', formation)
    #
    # formation.z.x = -28
    # library.add_formation_to_library('Twin Lt', formation)

    library.load_library('formations.scmfl')

    for label, formation in library.formations.items():
        print('\n')
        print(label)
        for label, player in formation.players.items():
            print('{}: {},{}'.format(player.label, player.x, player.y))

    library.save_library('formations.scmfl')
