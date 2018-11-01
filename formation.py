class Player:
    def __init__(self, label, x = 0, y = 0):
        self.label = label
        self.x = x
        self.y = y

class Formation:
    def __init__(self):
        self.lt = Player('LT', -8, 1)
        self.lg = Player('LG', -4, 1)
        self.c = Player('C', 0, 1)
        self.rg = Player('RG', 4, 1)
        self.rt = Player('RT', 8, 1)
        self.t = Player('T', 0, 7)
        self.h = Player('H', 0, 5)
        self.x = Player('X', -35, 1)
        self.y = Player('Y', 12, 1)
        self.z = Player('Z', 35, 2)
        self.q = Player('Q', 0, 2)
        self.players = {}
        self.players['LT'] = self.lt
        self.players['LG'] = self.lg
        self.players['C'] = self.c
        self.players['RG'] = self.rg
        self.players['RT'] = self.rt
        self.players['T'] = self.t
        self.players['H'] = self.h
        self.players['X'] = self.x
        self.players['Y'] = self.y
        self.players['Z'] = self.z
        self.players['Q'] = self.q
        self.is_override_formation = False
        self.override_player_tags = []

    def copy_formation_from_formation(self, copy_formation):
        for tag, player in copy_formation.players.items():
            self.players[tag].x = copy_formation.players[tag].x
            self.players[tag].y = copy_formation.players[tag].y
        self.override_player_tags = []
        for tag in copy_formation.override_player_tags:
            self.override_player_tags.append(tag)
        self.is_override_formation = copy_formation.is_override_formation


    def override_formation(self, override_formation):
        for tag in override_formation.override_player_tags:
            self.players[tag].x = override_formation.players[tag].x
            self.players[tag].y = override_formation.players[tag].y

    def flip_formation(self):
        for tag, player in self.players.items():
            if len(tag) == 1 and tag != 'C':
                player.x *= -1
