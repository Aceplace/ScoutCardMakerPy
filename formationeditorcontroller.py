import formation

class FormationEditorController:
    def __init__(self, formation):
        self.current_formation = formation

    def update_player_in_formation(self, tag, x, y):
        self.current_formation.players[tag].x = x
        self.current_formation.players[tag].y = y

    def print_player_positions(self):
        for key, player in self.current_formation.players.items():
            print("{} : {} , {}".format(player.label, player.x, player.y))
