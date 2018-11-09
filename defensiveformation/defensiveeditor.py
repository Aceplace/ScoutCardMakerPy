from tkinter import *

class DefensiveEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller

        defender_frame = Frame(self)
        defender_frame.pack(side=LEFT)

        Label(defender_frame, text='Current Defender :').grid(row=0, column=0, sticky=E)
        defender_names = self.controller.get_defender_names()
        self.current_defender_value = StringVar()
        self.current_defender_value.set(self.controller.current_defender.label)
        self.current_defender_om = OptionMenu(defender_frame, self.current_defender_value, *defender_names, command=self.change_defender)
        self.current_defender_om.grid(row=0, column=1, sticky=W+E)

        Label(defender_frame, text='Placement Rule :').grid(row=1, column=0, sticky=E)
        placement_rule_names = self.controller.get_placement_names()
        self.placement_rule_value = StringVar()
        self.placement_rule_value.set(controller.get_placement_rule_name_from_placement_rule(self.controller.current_defender.placement_rule))
        self.placement_rule_om = OptionMenu(defender_frame, self.placement_rule_value, *placement_rule_names, command=self.change_placement_rule)
        self.placement_rule_om.grid(row=1, column=1, sticky=W + E)

        placement_rule_frame = Frame(self)



    def change_defender(self, *args):
        pass

    def change_placement_rule(self, *args):
        pass

if __name__ == '__main__':
    from defensiveformation.defensiveeditorcontroller import DefensiveEditorController
    root = Tk()
    controller = DefensiveEditorController()
    DefensiveEditor(root, controller).pack()
    root.mainloop()

