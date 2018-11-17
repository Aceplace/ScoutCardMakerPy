from offensiveformation.formationutils import *
from tkinter import *
from defensiveformation.defensiveutils import BAD_PLACEMENT

class ApexType(Enum):
    TACKLE_AND_FIRST_RECEIVER = 0
    THREE_AND_TWO = 1
    TWO_AND_ONE = 2


class ApexPlacementRule():
    def __init__(self, apex_type = ApexType.TACKLE_AND_FIRST_RECEIVER, direction = Direction.STR,
                 strength_type = StrengthType.ATTACHED, depth=5):
        self.apex_type = apex_type
        self.direction = direction
        self.strength_type = strength_type
        self.depth = depth

    def place(self, formation):
        y = self.depth

        align_side = get_align_side(self.direction, self.strength_type, formation)
        receivers_inside_out = get_receivers_inside_out(formation, 'LT') if align_side == Direction.LEFT else get_receivers_inside_out(formation, 'RT')
        receivers_outside_in = get_receivers_outside_in(formation, 'LT') if align_side == Direction.LEFT else get_receivers_outside_in(formation, 'RT')

        if self.apex_type == ApexType.TACKLE_AND_FIRST_RECEIVER:
            if len(receivers_inside_out) >= 1:
                x = (receivers_inside_out[0].x + formation.lt.x) // 2 if align_side == Direction.LEFT else (receivers_inside_out[0].x + formation.rt.x) // 2
            else:
                x, y = BAD_PLACEMENT
        elif self.apex_type == ApexType.THREE_AND_TWO:
            if len(receivers_outside_in) >= 3:
                x = (receivers_outside_in[2].x + receivers_outside_in[1].x) // 2
            else:
                x, y = BAD_PLACEMENT
        else: #self.apex_type == ApexType.TWO_AND_ONE:
            if len(receivers_outside_in) >= 2:
                x = (receivers_outside_in[1].x + receivers_outside_in[0].x) // 2
            else:
                x, y = BAD_PLACEMENT

        return x, y


class ApexPlacementRuleGUI(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller


        Label(self, text='Apex Type:').grid(row=0, column=0, sticky=E)
        apex_type_names = [name for name, member in ApexType.__members__.items()]
        self.apex_type_value = StringVar()
        self.apex_type_value.set(apex_type_names[0])
        self.apex_type_om = OptionMenu(self, self.apex_type_value, *apex_type_names, command=self.update_defender)
        self.apex_type_om.grid(row=0, column=1, sticky=W+E)

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
        apex_placement_rule = self.controller.current_defender.placement_rule

        self.apex_type_value.set(apex_placement_rule.apex_type.name)
        self.direction_value.set(apex_placement_rule.direction.name)
        self.strength_type_value.set(apex_placement_rule.strength_type.name)
        self.depth_sb.configure(state=NORMAL)
        self.depth_sb.delete(0,END)
        self.depth_sb.insert(0, apex_placement_rule.depth)
        self.depth_sb.configure(state='readonly')


    def update_defender(self, *args):
        apex_type = ApexType[self.apex_type_value.get()]
        direction = Direction[self.direction_value.get()]
        strength_type = StrengthType[self.strength_type_value.get()]
        depth = int(self.depth_sb.get())

        alignment_placement_rule = ApexPlacementRule(apex_type, direction, strength_type, depth)
        self.controller.set_defender_placement_rule(alignment_placement_rule)


