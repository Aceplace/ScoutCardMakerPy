from defensiveformation.defense import Defense
from defensiveformation.alignmentplacementrule import *
from defensiveformation.overplacementrule import *

def get_default_defense():
    defense = Defense()
    defense.t.placement_rule = AlignmentPlacementRule(Alignment.THREE, Direction.STR, StrengthType.ATTACHED)
    defense.n.placement_rule = AlignmentPlacementRule(Alignment.ONE, Direction.WK, StrengthType.ATTACHED)
    defense.p.placement_rule = AlignmentPlacementRule(Alignment.FIVE, Direction.WK, StrengthType.ATTACHED)
    defense.a.placement_rule = AlignmentPlacementRule(Alignment.SIX_I, Direction.STR, StrengthType.ATTACHED)
    defense.f.placement_rule = OverPlacementRule(OverPlayerOption.OL_C, Leverage.HEAD_UP, Direction.STR,
                                              StrengthType.RECEIVER_STRENGTH, 12)
    defense.c.placement_rule = OverPlacementRule(OverPlayerOption.NUMBER_ONE, Leverage.INSIDE, Direction.STR,
                                              StrengthType.RECEIVER_STRENGTH, 8)
    defense.q.placement_rule = OverPlacementRule(OverPlayerOption.NUMBER_ONE, Leverage.OUTSIDE, Direction.WK,
                                              StrengthType.RECEIVER_STRENGTH, 7)
    return defense