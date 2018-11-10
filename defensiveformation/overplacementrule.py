from misc.formationutils import *
from tkinter import *

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
    def __init__(self, over_player_option = OverPlayerOption.NUMBER_ONE,
                 leverage = Leverage.HEAD_UP, direction = Direction.STR,
                 strength_type = StrengthType.RECEIVER_STRENGTH, depth=5):
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


class OverPlacementRuleGUI(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller

        Label(self, text='Over Option:').grid(row=0, column=0, sticky=E)
        over_option_names = [name for name, member in OverPlayerOption.__members__.items()]
        self.over_option_value = StringVar()
        self.over_option_value.set(over_option_names[0])
        self.over_option_om = OptionMenu(self, self.over_option_value, *over_option_names, command=self.update_defender)
        self.over_option_om.grid(row=0, column=1, sticky=W+E)

        Label(self, text='Leverage:').grid(row=1, column=0, sticky=E)
        leverage_names = [name for name, member in Leverage.__members__.items()]
        self.leverage_value = StringVar()
        self.leverage_value.set(leverage_names[0])
        self.leverage_om = OptionMenu(self, self.leverage_value, *leverage_names, command=self.update_defender)
        self.leverage_om.grid(row=1, column=1, sticky=W + E)

        Label(self, text='Direction:').grid(row=2, column=0, sticky=E)
        direction_names = [name for name, member in Direction.__members__.items()]
        self.direction_value = StringVar()
        self.direction_value.set(direction_names[0])
        self.direction_om = OptionMenu(self, self.direction_value, *direction_names, command=self.update_defender)
        self.direction_om.grid(row=2, column=1, sticky=W+E)

        Label(self, text='Strength Type:').grid(row=3, column=0, sticky=E)
        strength_type_names = [name for name, member in StrengthType.__members__.items()]
        self.strength_type_value = StringVar()
        self.strength_type_value.set(strength_type_names[0])
        self.strength_type_om = OptionMenu(self, self.strength_type_value, *strength_type_names, command=self.update_defender)
        self.strength_type_om.grid(row=3, column=1, sticky=W+E)

        Label(self, text='Depth:').grid(row=3, column=0, sticky=E)
        self.depth_sb = Spinbox(self, from_ = 1 , to_ = 15, state='readonly', command=self.update_defender)
        self.depth_sb.grid(row=3, column=1, sticky=W+E)

        self.update_gui_with_defender_info()


    def update_gui_with_defender_info(self):
        over_placement_rule = self.controller.current_defender.placement_rule

        self.over_option_value.set(over_placement_rule.over_player_option.name)
        self.leverage_value.set(over_placement_rule.leverage.name)
        self.direction_value.set(over_placement_rule.direction.name)
        self.strength_type_value.set(over_placement_rule.strength_type.name)
        self.depth_sb.configure(state=NORMAL)
        self.depth_sb.delete(0,END)
        self.depth_sb.insert(0, over_placement_rule.depth)
        self.depth_sb.configure(state='readonly')


    def update_defender(self, *args):
        over_player_option = OverPlayerOption[self.over_option_value.get()]
        leverage = Leverage[self.leverage_value.get()]
        direction = Direction[self.direction_value.get()]
        strength_type = StrengthType[self.strength_type_value.get()]
        depth = int(self.depth_sb.get())

        alignment_placement_rule = OverPlacementRule(over_player_option, leverage, direction, strength_type, depth)
        self.controller.set_defender_placement_rule(alignment_placement_rule)





if __name__=='__main__':
    from defensiveformation.defensiveutils import *
    class MockController():
        def __init__(self):
            self.defense = get_default_defense()
            self.current_defender = self.defense.c

        def set_defender_placement_rule(self, placement_rule):
            self.current_defender = self.current_defender.placement_rule = placement_rule


    root = Tk()
    controller = MockController()
    gui = OverPlacementRuleGUI(root, controller)
    gui.pack()
    root.mainloop()