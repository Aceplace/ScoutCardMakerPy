from placementrules import *

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
        self.t.placement_rule = AlignmentPlacementRule(Alignment.THREE, Direction.STR, StrengthType.ATTACHED)
        self.n = Defender('N')
        self.n.placement_rule = AlignmentPlacementRule(Alignment.ONE, Direction.WK, StrengthType.ATTACHED)
        self.p = Defender('P')
        self.p.placement_rule = AlignmentPlacementRule(Alignment.FIVE, Direction.WK, StrengthType.ATTACHED)
        self.a = Defender('A')
        self.a.placement_rule = AlignmentPlacementRule(Alignment.SIX_I, Direction.STR, StrengthType.ATTACHED)
        self.w = Defender('W')
        self.m = Defender('M')
        self.b = Defender('B')
        self.s = Defender('S')
        self.f = Defender('F')
        self.f.placement_rule = OverPlacementRule(OverPlayerOption.OL_C, Leverage.HEAD_UP, Direction.STR, StrengthType.RECEIVER_STRENGTH, 12)
        self.c = Defender('C')
        self.c.placement_rule = OverPlacementRule(OverPlayerOption.NUMBER_ONE, Leverage.INSIDE, Direction.STR, StrengthType.RECEIVER_STRENGTH, 8)
        self.q = Defender('Q')
        self.q.placement_rule = OverPlacementRule(OverPlayerOption.NUMBER_ONE, Leverage.OUTSIDE, Direction.WK, StrengthType.RECEIVER_STRENGTH, 7)
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
        self.affected_defender_tags = []

if __name__=='__main__':
    pass