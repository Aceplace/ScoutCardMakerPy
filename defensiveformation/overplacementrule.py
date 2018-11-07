from misc.formationutils import *

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
