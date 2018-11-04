from enum import Enum
from formationutils import *

class Alignment(Enum):
    ZERO = 0
    ONE = 1
    TWO_I = 2
    TWO = 3
    THREE = 4
    FOUR_I = 5
    FOUR = 6
    FIVE = 7
    FIVE_I = 8
    SIX = 9
    SIX_I = 10
    SEVEN = 11
    EIGHT_I = 12
    EIGHT = 13
    NINE = 14

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    STR = 3
    WK = 4

class StrengthType(Enum):
    ATTACHED = 1
    RECEIVER_STRENGTH = 2


def get_align_side(direction, strength_type, formation):
    if direction == Direction.LEFT or direction == Direction.RIGHT:
        return direction

    if strength_type == StrengthType.ATTACHED:
        strength_direction = get_attached_receiver_strength(formation)
    else:
        strength_direction = get_receiver_strength(formation)

    if strength_direction == 'LT':
        if direction == Direction.STR:
            return Direction.LEFT
        else:
            return Direction.RIGHT
    else:
        if direction == Direction.STR:
            return Direction.RIGHT
        else:
            return Direction.LEFT

class AlignmentPlacementRule():
    def __init__(self, alignment, direction, strength_type, depth=1):
        self.alignment = alignment
        self.direction = direction
        self.strength_type = strength_type
        self.depth = depth

    def place(self, formation):
        y = self.depth

        if self.alignment == Alignment.ZERO:
            x = 0

        align_side = get_align_side(self.direction, self.strength_type, formation)
        #modifier is negative one on left side to move players the appropriate direction
        flip = 1 if align_side == Direction.RIGHT else -1

        if self.alignment == Alignment.ONE:
            align_player = formation.c
            x = align_player.x + flip
        elif self.alignment == Alignment.TWO_I:
            align_player = formation.lg if align_side == Direction.LEFT else formation.rg
            x = align_player.x - flip
        elif self.alignment == Alignment.TWO:
            align_player = formation.lg if align_side == Direction.LEFT else formation.rg
            x = align_player.x
        elif self.alignment == Alignment.THREE:
            align_player = formation.lg if align_side == Direction.LEFT else formation.rg
            x = align_player.x + flip
        elif self.alignment == Alignment.FOUR_I:
            align_player = formation.lt if align_side == Direction.LEFT else formation.rt
            x = align_player.x - flip
        elif self.alignment == Alignment.FOUR:
            align_player = formation.lt if align_side == Direction.LEFT else formation.rt
            x = align_player.x
        elif self.alignment == Alignment.FIVE:
            align_player = formation.lt if align_side == Direction.LEFT else formation.rt
            x = align_player.x + flip
        elif self.alignment == Alignment.SIX_I:
            align_player = get_first_attached(formation, 'LT') if align_side == Direction.LEFT else get_first_attached(formation, 'RT')
            if align_player:
                x = align_player.x - flip
            else:
                x = (formation.rt.x + GHOST_DISTANCE) * flip
        elif self.alignment == Alignment.SIX:
            align_player = get_first_attached(formation, 'LT') if align_side == Direction.LEFT else get_first_attached(formation, 'RT')
            if align_player:
                x = align_player.x - flip
            else:
                x = (formation.rt.x + GHOST_DISTANCE) * flip
        elif self.alignment == Alignment.SEVEN:
            align_player = get_first_attached(formation, 'LT') if align_side == Direction.LEFT else get_first_attached(formation, 'RT')
            if align_player:
                x = align_player.x - flip
            else:
                x = (formation.rt.x + GHOST_DISTANCE) * flip
        elif self.alignment == Alignment.EIGHT_I:
            align_player = get_second_attached(formation, 'LT') if align_side == Direction.LEFT else get_second_attached(formation, 'RT')
            if align_player:
                x = align_player.x - flip
            else:
                x = (formation.rt.x + GHOST_DISTANCE * 2) * flip
        elif self.alignment == Alignment.EIGHT:
            align_player = get_second_attached(formation, 'LT') if align_side == Direction.LEFT else get_second_attached(formation, 'RT')
            if align_player:
                x = align_player.x - flip
            else:
                x = (formation.rt.x + GHOST_DISTANCE * 2) * flip
        elif self.alignment == Alignment.NINE:
            align_player = get_second_attached(formation, 'LT') if align_side == Direction.LEFT else get_second_attached(formation, 'RT')
            if align_player:
                x = align_player.x - flip
            else:
                x = (formation.rt.x + GHOST_DISTANCE * 2) * flip

        return x, y

class OverPlayerOption(Enum):
    NUMBER_ONE = 1
    NUMBER_TWO = 2
    NUMBER_THREE = 3
    NUMBER_FOUR = 4
    NUMBER_FIVE = 5
    T = 9
    H = 10
    X = 11
    Y = 12
    Z = 13
    Q = 14
    OL_T = 15
    OL_G = 16
    OL_C = 17

class Leverage(Enum):
    INSIDE = 1
    HEAD_UP = 2
    OUTSIDE = 3

class OverPlacementRule:
    def __init__(self, over_player_option, leverage, direction, strength_type, depth=5):
        self.over_player_option = over_player_option
        self.leverage = leverage
        self.direction = direction
        self.strength_type = strength_type
        self.depth = depth

    def place(self, formation):
        y = self.depth

        align_side = get_align_side(self.direction, self.strength_type, formation)
        receiver_outside_in = get_receivers_outside_in(formation, 'LT' if align_side == Direction.LEFT else 'RT')
        if self.leverage == Leverage.INSIDE:
            leverage_adjust = 1 if align_side == Direction.LEFT else -1
        elif self.leverage == Leverage.OUTSIDE:
            leverage_adjust = 1 if align_side == Direction.RIGHT else 1
        else:
            leverage_adjust = 0

        if self.over_player_option == OverPlayerOption.NUMBER_ONE:
            x = receiver_outside_in[0].x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.NUMBER_TWO:
            x = receiver_outside_in[1].x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.NUMBER_THREE:
            x = receiver_outside_in[2].x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.NUMBER_FOUR:
            x = receiver_outside_in[3].x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.NUMBER_FIVE:
            x = receiver_outside_in[4].x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.T:
            x = formation.t.x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.H:
            x = formation.h.x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.X:
            x = formation.x.x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.Y:
            x = formation.y.x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.Z:
            x = formation.z.x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.Q:
            x = formation.q.x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.OL_C:
            x = formation.c.x + leverage_adjust
        elif self.over_player_option == OverPlayerOption.OL_T:
            if align_side == Direction.LEFT:
                x = formation.lt.x + leverage_adjust
            else:
                x = formation.rt.x + leverage_adjust
        else:
            if align_side == Direction.LEFT:
                x = formation.lg.x + leverage_adjust
            else:
                x = formation.rg.x + leverage_adjust

        return x, y


if __name__=='__main__':
    pass