from misc.formationutils import *
from tkinter import *

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

class AlignmentPlacementRule():
    def __init__(self, alignment = Alignment.THREE, direction = Direction.STR,
                 strength_type = StrengthType.ATTACHED, depth=1):
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


class AlignmentPlacementRuleGUI(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller


        Label(self, text='Alignment:').grid(row=0, column=0, sticky=E)
        alignment_names = [name for name, member in Alignment.__members__.items()]
        self.alignment_value = StringVar()
        self.alignment_value.set(alignment_names[0])
        self.alignment_om = OptionMenu(self, self.alignment_value, *alignment_names, command=self.update_defender)
        self.alignment_om.grid(row=0, column=1, sticky=W+E)

        Label(self, text='Direction:').grid(row=1, column=0, sticky=E)
        direction_names = [name for name, member in Direction.__members__.items()]
        self.direction_value = StringVar()
        self.direction_value.set(direction_names[0])
        self.direction_om = OptionMenu(self, self.direction_value, *direction_names, command=self.update_defender)
        self.direction_om.grid(row=1, column=1, sticky=W+E)

        Label(self, text='Strength Type:').grid(row=2, column=0, sticky=E)
        strength_type_names = [name for name, member in StrengthType.__members__.items()]
        self.strength_type_value = StringVar()
        self.strength_type_value.set(strength_type_names[0])
        self.strength_type_om = OptionMenu(self, self.strength_type_value, *strength_type_names, command=self.update_defender)
        self.strength_type_om.grid(row=2, column=1, sticky=W+E)

        Label(self, text='Depth:').grid(row=3, column=0, sticky=E)
        self.depth_sb = Spinbox(self, from_ = 1 , to_ = 15, state='readonly', command=self.update_defender)
        self.depth_sb.grid(row=3, column=1, sticky=W+E)

        self.update_gui_with_defender_info()


    def update_gui_with_defender_info(self):
        alignment_placement_rule = self.controller.current_defender.placement_rule

        self.alignment_value.set(alignment_placement_rule.alignment.name)
        self.direction_value.set(alignment_placement_rule.direction.name)
        self.strength_type_value.set(alignment_placement_rule.strength_type.name)
        self.depth_sb.configure(state=NORMAL)
        self.depth_sb.delete(0,END)
        self.depth_sb.insert(0, alignment_placement_rule.depth)
        self.depth_sb.configure(state='readonly')


    def update_defender(self, *args):
        alignment = Alignment[self.alignment_value.get()]
        direction = Direction[self.direction_value.get()]
        strength_type = StrengthType[self.strength_type_value.get()]
        depth = int(self.depth_sb.get())

        alignment_placement_rule = AlignmentPlacementRule(alignment, direction, strength_type, depth)
        self.controller.set_defender_placement_rule(alignment_placement_rule)


