from tkinter import *
import random
from defensiveformation.placementrules.conditions import condition_name_condition_dict
from defensiveformation.placementrules.placementruleutils import *



class ConditionPlacement:
    def __init__(self):
        self.condition = random.choice(list(condition_name_condition_dict.keys()))
        self.placement_rule = AlignmentPlacementRule()

class ConditionalPlacementRule:
    def __init__(self):
        self.condition_rules = []

    def place(self, formation):
        x, y = None, None
        for condition in self.condition_rules:
            if condition.evaluate_condition():
                x, y = condition.placement_rule.place(formation)
        if not x or not y:
            x , y = -20, 14 #magic numbers to just throw the guy somewhere on the field

        return x, y


class ConditionalPlacementRuleGUI(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E + W)
        self.canvas = Canvas(self, bd=0, xscrollcommand=xscrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        xscrollbar.config(command=self.canvas.xview)

        self.condition_frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.condition_frame, anchor=N+W)
        self.condition_frame.bind("<Configure>", self.on_frame_configure)

        Button(self.condition_frame, text='Add Condition', command=self.add_condition).grid(row=0, column=0)
        self.populate_condition_gui()

        self.update_gui_with_defender_info()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_gui_with_defender_info(self):
        pass

    def update_defender(self, *args):
        pass

    def populate_condition_gui(self):
        conditional_rule = self.controller.current_defender.placement_rule

        #create a gui for each condition placement rule
        sub_guis = []
        for index in range(len(conditional_rule.condition_rules)):
            sub_guis.append(SubconditionalPlacementRuleGUI(self.condition_frame, conditional_rule.condition_rules[index]))
            sub_guis[index].grid(row=0, column=index+1)

    def add_condition(self):
        pass


class SubconditionalPlacementRuleGUI(Frame):
    def __init__(self, root, parent_rule, condition_placement):
        Frame.__init__(self, root)
        self.parent_rule = parent_rule
        self.condition_placement = condition_placement

        condition_rule_frame = Frame(self)
        condition_rule_frame.pack(side=LEFT)

        Label(condition_rule_frame, text='Condition:').grid(row=0, column=0, sticky=E)
        condition_names = [name for name, condition in condition_name_condition_dict.items() ]
        self.condition_value = StringVar()
        self.condition_value.set(self.condition_placement.condition)
        self.conditon_value_om = OptionMenu(condition_rule_frame, self.condition_value, *condition_names,
                                              command=self.change_condition)
        self.conditon_value_om.grid(row=0, column=1, sticky=W + E)

        Label(condition_rule_frame, text='Placement Rule :').grid(row=1, column=0, sticky=E)
        placement_rule_names = [name for name, rule in placement_type_dict.items() if name !='Conditional']
        self.placement_rule_name_value = StringVar()
        self.placement_rule_name_value.set(placement_type_name_dict[type(self.condition_placement.placement_rule)])
        self.placement_rule_om = OptionMenu(condition_rule_frame, self.placement_rule_name_value, *placement_rule_names,
                                            command=self.change_placement_rule)
        self.placement_rule_om.grid(row=1, column=1, sticky=W + E)

        Button(condition_rule_frame, text='Raise Priority', command=self.raise_priority).grid(row=2, column=0, columnspan=2)
        Button(condition_rule_frame, text='Lower Priority', command=self.lower_priority).grid(row=3, column=0, columnspan=2)
        Button(condition_rule_frame, text='Delete Condition', command=self.delete_condition).grid(row=4, column=0, columnspan=2)

        self.current_defender = self.condition_placement
        # The above is needed because placement rule gui's require a controller with a current_defender property
        # which itself has a placement_rule property (which condition_placement does have)
        self.placement_rule_frame = Frame(self)
        self.placement_rule_frame.pack(side=RIGHT)
        placement_rule_gui_type = placement_type_gui_dict[type(self.condition_placement.placement_rule)]
        self.placement_rule_gui = placement_rule_gui_type(self.placement_rule_frame, self)
        self.placement_rule_gui.pack()

        self.update_sub_gui_with_condition_placement_info()

    def update_sub_gui_with_condition_placement_info(self):
        self.placement_rule_gui.update_gui_with_defender_info()

    def change_condition(self, *args):
        self.condition_placement.condition = self.condition_value.get()

    def change_placement_rule(self, *args):
        placement_rule = placement_type_dict[self.placement_rule_name_value.get()]()
        self.condition_placement.placement_rule = placement_rule
        #switch out the gui for the proper placement rule gui
        self.placement_rule_gui.pack_forget()
        self.placement_rule_gui.destroy()
        placement_rule_gui_type = placement_type_gui_dict[type(self.condition_placement.placement_rule)]
        self.placement_rule_gui = placement_rule_gui_type(self.placement_rule_frame, self)
        self.placement_rule_gui.pack()


    def raise_priority(self):
        self.parent_rule.raise_priority(self.condition_placement)

    def lower_priority(self):
        self.parent_rule.lower_priority(self.condition_placement)

    def delete_condition(self):
        self.parent_rule.delete_condition(self.condition_placement)

    #this method is required because the placement rule guis expect it
    def set_defender_placement_rule(self, placement_rule):
        self.condition_placement.placement_rule = placement_rule


if __name__ == '__main__':
    root = Tk()
    class MockController():
        def __init__(self):
            from defensiveformation.defense import Defender
            self.current_defender = Defender('T')
            self.current_defender.placement_rule = ConditionalPlacementRule()

    ConditionalPlacementRuleGUI(root, MockController()).pack(fill=X, expand=TRUE)
    root.mainloop()