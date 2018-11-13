from offensiveformation.formationutils import get_formation_structure
from tkinter import *

condition_name_condition_evaluate_dict ={
    'Default': lambda formation: True,
    'Formation Structure/1x1' : lambda formation: formation_structure_condition(formation, '1x1'),
    'Formation Structure/2x1' : lambda formation: formation_structure_condition(formation, '2x1'),
    'Formation Structure/2x2' : lambda formation: formation_structure_condition(formation, '2x2'),
    'Formation Structure/3x1' : lambda formation: formation_structure_condition(formation, '3x1'),
    'Formation Structure/3x2' : lambda formation: formation_structure_condition(formation, '3x2'),
    'Formation Structure/4x1' : lambda formation: formation_structure_condition(formation, '4x1')
}

def formation_structure_condition(formation, formation_structure):
    return formation_structure == get_formation_structure(formation)


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


if __name__=='__main__':
    root = Tk()
    ConditionsMenu(root, None).pack()
    root.mainloop()
