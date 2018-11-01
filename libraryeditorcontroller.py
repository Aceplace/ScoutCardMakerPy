from formation import Formation

class LibraryEditorController:
    def __init__(self, formation_library):
        self.current_formation = Formation()
        self.formation_library = formation_library

    def update_player_in_formation(self, tag, x, y):
        self.current_formation.players[tag].x = x
        self.current_formation.players[tag].y = y

    def load_formation_from_library(self, formation_name):
        formation = self.formation_library.get_formation(formation_name)
        self.current_formation.copy_formation_from_formation(formation)

    def load_composite_formation_from_library(self, formation_name):
        formation = self.formation_library.get_composite_formation(formation_name)
        self.current_formation.copy_formation_from_formation(formation)

    def save_formation_to_library(self, formation_name, is_override_formation, override_player_tags):
        self.current_formation.is_override_formation = is_override_formation
        self.current_formation.override_player_tags = override_player_tags
        self.formation_library.add_formation_to_library(formation_name, self.current_formation)

    def print_player_positions(self):
        for key, player in self.current_formation.players.items():
            print("{} : {} , {}".format(player.label, player.x, player.y))
