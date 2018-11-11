class Defender:
    def __init__(self, label):
        self.label = label
        self.placement_rule = None

    def place_defender(self, formation):
        if self.placement_rule:
            return self.placement_rule.place(formation)
        return (0,1)

class Defense:
    def __init__(self):
        self.t = Defender('T')
        self.n = Defender('N')
        self.p = Defender('P')
        self.a = Defender('A')
        self.w = Defender('W')
        self.m = Defender('M')
        self.b = Defender('B')
        self.s = Defender('S')
        self.f = Defender('F')
        self.c = Defender('C')
        self.q = Defender('Q')
        self.defenders = {}
        self.defenders['T'] = self.t
        self.defenders['N'] = self.n
        self.defenders['P'] = self.p
        self.defenders['A'] = self.a
        self.defenders['W'] = self.w
        self.defenders['M'] = self.m
        self.defenders['B'] = self.b
        self.defenders['S'] = self.s
        self.defenders['F'] = self.f
        self.defenders['C'] = self.c
        self.defenders['Q'] = self.q
        self.affected_defender_tags = ['T','C']

    def copy_defense_from_defense(self, copy_defense):
        for tag, defender in copy_defense.defenders.items():
            self.defenders[tag].placement_rule = copy_defense.defenders[tag].placement_rule
        self.affected_defender_tags = []
        for tag in copy_defense.affected_defender_tags:
            self.affected_defender_tags.append(tag)

    def override_defense(self, override_defense):
        for tag in override_defense.affected_defender_tags:
            self.defenders[tag].placement_rule = override_defense.defenders[tag].placement_rule
