from offensiveformation.formation import Formation
from offensiveformation.formationlibrary import FormationLibrary

class FormationLibraryEditorController:
    def __init__(self):
        self.current_formation = Formation()
        self.formation_library = FormationLibrary()
        self.editor = None

    def update_player_in_formation(self, tag, x, y):
        self.current_formation.players[tag].x = x
        self.current_formation.players[tag].y = y

    def load_formation_from_library(self, formation_name):
        formation = self.formation_library.get_formation(formation_name)
        self.current_formation.copy_formation_from_formation(formation)

    def load_composite_formation_from_library(self, formation_name):
        formation = self.formation_library.get_composite_formation(formation_name)
        self.current_formation.copy_formation_from_formation(formation)

    def save_formation_to_library(self, formation_name, affected_player_tags):
        self.current_formation.affected_player_tags = affected_player_tags
        self.formation_library.add_formation_to_library(formation_name, self.current_formation)

    def delete_formation_from_library(self, formation_name):
        self.formation_library.delete_formation_from_library(formation_name)

    def new_library(self):
        self.formation_library = FormationLibrary()
        if self.editor:
            self.editor.refresh_library()

    def load_library(self, library_filename):
        self.formation_library.load_library(library_filename)
        if self.editor:
            self.editor.refresh_library()

    def save_library(self, library_filename):
        self.formation_library.save_library(library_filename)

    def print_player_positions(self):
        for key, player in self.current_formation.players.items():
            print("{} : {} , {}".format(player.label, player.x, player.y))
