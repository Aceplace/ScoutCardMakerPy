from formation import Formation

class LibraryEditorController:
    def __init__(self, formation_library):
        self.current_formation = Formation()
        self.formation_library = formation_library

    def update_player_in_formation(self, tag, x, y):
        self.current_formation.players[tag].x = x
        self.current_formation.players[tag].y = y

    def print_player_positions(self):
        for key, player in self.current_formation.players.items():
            print("{} : {} , {}".format(player.label, player.x, player.y))
