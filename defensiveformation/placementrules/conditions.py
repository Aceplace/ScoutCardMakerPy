from offensiveformation.formationutils import get_formation_structure, Direction, StrengthType, get_align_side, get_surface_structures
from tkinter import *

condition_name_condition_evaluate_dict ={
    'Default': lambda formation: True,
    'Formation Structure/1x1' : lambda formation: formation_structure_condition(formation, '1x1'),
    'Formation Structure/2x1' : lambda formation: formation_structure_condition(formation, '2x1'),
    'Formation Structure/2x2' : lambda formation: formation_structure_condition(formation, '2x2'),
    'Formation Structure/3x1' : lambda formation: formation_structure_condition(formation, '3x1'),
    'Formation Structure/3x2' : lambda formation: formation_structure_condition(formation, '3x2'),
    'Formation Structure/4x1' : lambda formation: formation_structure_condition(formation, '4x1'),
    'Surface Structure (Rec Str)/Zero Receivers' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Zero Receivers']),
    'Surface Structure (Rec Str)/One Receiver' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['One Receiver']),
    'Surface Structure (Rec Str)/Two Receivers' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Two Receivers']),
    'Surface Structure (Rec Str)/Three Receivers' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Three Receivers']),
    'Surface Structure (Rec Str)/Four Receivers' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Four Receivers']),
    'Surface Structure (Rec Str)/Five Receivers' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Five Receivers']),
    'Surface Structure (Rec Str)/Nub' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Nub']),
    'Surface Structure (Rec Str)/Split' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Split']),
    'Surface Structure (Rec Str)/Twin' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Twin']),
    'Surface Structure (Rec Str)/Pro' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Pro']),
    'Surface Structure (Rec Str)/Wing' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Wing']),
    'Surface Structure (Rec Str)/Trips' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Trips']),
    'Surface Structure (Rec Str)/Indy' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Indy']),
    'Surface Structure (Rec Str)/Indy Wing' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Indy Wing']),
    'Surface Structure (Rec Str)/Tight Bunch' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Tight Bunch']),
    'Surface Structure (Rec Wk)/Zero Receivers' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['Zero Receivers']),
    'Surface Structure (Rec Wk)/One Receiver' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['One Receiver']),
    'Surface Structure (Rec Wk)/Two Receivers' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['Two Receivers']),
    'Surface Structure (Rec Wk)/Nub' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['Nub']),
    'Surface Structure (Rec Wk)/Split' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['Split']),
    'Surface Structure (Rec Wk)/Twin' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['Twin']),
    'Surface Structure (Rec Wk)/Pro' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['Pro']),
    'Surface Structure (Rec Wk)/Wing' : lambda formation: surface_structure_condition(formation, Direction.WK, StrengthType.RECEIVER_STRENGTH, ['Wing']),
    'Surface Structure (Rec Wk)/Trips' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Trips']),
    'Surface Structure (Rec Wk)/Indy' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Indy']),
    'Surface Structure (Rec Wk)/Indy Wing' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Indy Wing']),
    'Surface Structure (Rec Wk)/Tight Bunch' : lambda formation: surface_structure_condition(formation, Direction.STR, StrengthType.RECEIVER_STRENGTH, ['Tight Bunch']),
}

def formation_structure_condition(formation, formation_structure):
    return formation_structure == get_formation_structure(formation)

def surface_structure_condition(formation, direction, strength_type, acceptable_surface_structures):
    align_side = get_align_side(direction, strength_type, formation)
    direction_str = 'LT' if align_side == Direction.LEFT else 'RT'

    surface_structures = get_surface_structures(formation, direction_str)
    return any(structure in acceptable_surface_structures for structure in surface_structures)


class ConditionsMenu(Frame):
    def __init__(self, root, parent_gui, string_var):
        Frame.__init__(self, root)
        self.parent_gui = parent_gui

        self.conditions_menu_value = string_var
        menubutton = Menubutton(self, textvariable=self.conditions_menu_value, indicatoron=True, borderwidth=1, relief="raised")
        main_menu = Menu(menubutton, tearoff=False)
        menubutton.configure(menu=main_menu)

        sub_menus = {}
        for name, condition_function in condition_name_condition_evaluate_dict.items():
            split_name = name.split('/')
            if len(split_name) == 1:
                main_menu.add_radiobutton(value=name, label=name, variable=self.conditions_menu_value, command=self.change_condition)
            else:
                if split_name[0] in sub_menus.keys():
                    sub_menus[split_name[0]].add_radiobutton(value=name, label=split_name[1], variable=self.conditions_menu_value, command=self.change_condition)
                else:
                    menu = Menu(main_menu, tearoff=False)
                    main_menu.add_cascade(label=split_name[0], menu=menu)
                    menu.add_radiobutton(value=name, label=split_name[1], variable=self.conditions_menu_value, command=self.change_condition)
                    sub_menus[split_name[0]] = menu
        main_menu.add_radiobutton(value='Delete Condition', label='Delete Condition', variable=self.conditions_menu_value, command=self.change_condition)
        menubutton.pack()

    def change_condition(self):
        self.parent_gui.change_condition(self.conditions_menu_value.get())

