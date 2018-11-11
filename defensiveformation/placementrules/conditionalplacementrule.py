from tkinter import *
from enum import Enum

from defensiveformation.placementrules.alignmentplacementrule import AlignmentPlacementRule


class Condition:
    def __init__(self):
        self.condition = None
        self.placement_rule = None

class ConditionalPlacementRule:
    def __init__(self):
        self.conditions = []
        self.default_placement_rule = AlignmentPlacementRule()

    def place(self, formation):
        x, y = None, None
        for condition in self.conditions:
            if condition.evaluate_condition():
                x, y = condition.placement_rule.place(formation)
        if not x or not y:
            x , y = self.default_placement_rule.place(formation)

        return x, y


class ConditionalPlacementRuleGUI(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E + W)
        self.canvas = Canvas(self, bd=0, xscrollcommand=xscrollbar.set, background='white', scrollregion=(0, 0, 1200, 800))
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        xscrollbar.config(command=self.canvas.xview)

        self.condition_frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.condition_frame, anchor=N+W)
        self.condition_frame.bind("<Configure>", self.on_frame_configure)

        self.update_gui_with_defender_info()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_gui_with_defender_info(self):
        pass


    def update_defender(self, *args):
        pass


if __name__ == '__main__':
    root = Tk()
    ConditionalPlacementRuleGUI(root, None).pack()
    root.mainloop()